"""This modules Defines all neo4j OGM models
"""
import hashlib
import relationships as rl

from py2neo.data import Node

class Branch(Node):
  """Branch node - currently not used
  """
  def __init__(self, kwargs):
    """
    :param kwargs:
    """
    Node.__init__(self, **kwargs)
    self.__dict__.update(locals())
    del self.self
    self.commits = []

  def add_commit(self, commit):
    """
    :param commit
    """
    self.commits.append(commit)


class Commit(Node):
  """Commit OGM  - Mapps Commit from PyDriller to py2neo
  """

  def __init__(self, commit):
    """Instantiates a commit. Please be aware the commit
    is not indexed on init. It is indexed when the first
    relation node (e.g. author/date) is indexed
    :param commit
    """
    self.commit = commit
    self.changes = []
    self.indexed = False
    Node.__init__(self, "Commit", hash=self.commit.hash)

  def _get_changes(self):
    """Parses and instantiate all files changed in
    this commit
    :returns: array of Changes objects
    """
    if len(self.changes) < 0:
      for chg in self.commit.modifications:
        self.changes.append(Change(chg))
    return self.changes

  def index_author(self, graph):
    """Indexes the commit author node in the graph
    and adds relationship to this commit
    :params graph: py2neo graph object
    """
    self.check_self(graph)
    dev = Developer(self.commit.author)
    graph.merge(dev, "Developer", "email")
    rel = rl.Authorship(dev, self)
    graph.create(rel)

  def index_parents(self, graph, repo):
    """For each parent of the commit, this method requests
    a commit object from pydriller's RepositoryMining object
    and indexes some data. If index_all is used, this method
    is applied recursively to all parents, however, this is
    very slow.
    :param graph: py2neo graph object
    :param repo: PyDriller RepositoryMining class for the
      current repo
    """
    self.check_self(graph)
    for parent in self.commit.parents:
      commit = Commit(repo.get_commit(parent))
      commit.index_author(graph)
      commit.index_date(graph)
      # commit.index_all(graph, repo)
      rel = rl.Parent(commit, self)
      graph.create(rel)

  def index_date(self, graph):
    """Splits the date in year, month and day and creates
    the graph nodes and relationships
    :param graph: py2neo graph object
    """
    self.check_self(graph)
    date = self.commit.author_date
    day = Day(date)
    month = Month(date)
    year = Year(date)
    graph.merge(year, "Year", "name")
    graph.merge(month, "Month", "hash")
    graph.merge(day, "Day", "hash")
    graph.create(rl.YearMonth(year, month))
    graph.create(rl.MonthDay(month, day))
    graph.create(rl.DayCommit(day, self))


  def check_self(self, graph):
    """Checks if the node corresponding to this instance
    is indexed in the database
    :param graph: py2neo graph object
    """
    if not self.indexed:
      graph.merge(self, "Commit", "hash")

  def index_all(self, graph, repo):
    """Indexes all the data for a commit
    :param graph: py2neo graph object
    :param repo: PyDriller RepositoryMining class for the
      current repo
    """
    self.check_self(graph)
    self.index_author(graph)
    self.index_date(graph)
    self.index_parents(graph, repo)


class Change(Node):
  """Change OGM Node - Maps files changed in a commit
  to py2neo objects
  """
  def __init__(self, change):
    """Instantiates change object. Please be aware the
    node is not created in the graph until a relationship
    is created. This avoids hanging nodes.
    :param change
    """
    self.change = change
    Node.__init__(self, "Change")


class Developer(Node):
  """Developer OGM Node - Maps PyDriller Developer objects
  to py2neo. Should be changed to Contributor in the future
  """

  def __init__(self, actor):
    """Instantiates a developer object. Please be aware the node
    is not created in the graph until a relationship
    is created. This avoids hanging nodes.
    :param actor:
    """
    self.actor = actor
    Node.__init__(self, "Developer",  name=self.actor.name, email=self.actor.email)


class Year(Node):
  """Year OGM node
  """
  def __init__(self, date):
    """Instantiates a year object. Please be aware the node
    is not created in the graph until a relationship
    is created. This avoids hanging nodes.
    :param date: datetime object containing all date info
    """
    Node.__init__(self, "Year", name=date.year)

class Month(Node):
  """Month node
  """
  def __init__(self, date):
    """Instantiates a month object and creates an unique
    hash for each month of each year. This model was chosen
    because we aim to represent time series. Please be aware
    the node is not created in the graph until a relationship
    is created. This avoids hanging nodes.
    :param date:: datetime object containing all date info
    """
    _hash = hashlib.sha224((str(date.month) + str(date.year)).encode('utf-8')).hexdigest()
    Node.__init__(self, "Month", name=date.month, hash=_hash)

class Day(Node):
  """Day node
  """
  def __init__(self, date):
    """Instantiates a day object and hashes the month, year and
    day as an unique key for the day. We wish to simulate a time
    series (otherwise, each month could've connect to the same day).
    Please be aware the node is not created in the graph until a
    relationship is created. This avoids hanging nodes.
    :param date: datetime object containing all date info
    """
    _hash = hashlib.sha224((str(date.month) + str(date.year) + str(date.day)).encode('utf-8')).hexdigest()
    Node.__init__(self, "Day", name=date.day, hash=_hash)
