"""This modules Defines all neo4j OGM models
"""
import hashlib
import relationships as rel

from py2neo.data import Node

class CustomNode(Node):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.indexed = False

  def check_self(self, graph):
    """Checks if the node corresponding to this instance
    is indexed in the database
    :param graph: py2neo graph object
    """
    if not self.indexed:
      graph.merge(self, self.node_type, self.node_index)
      self.indexed = True

class Branch(CustomNode):
  """Branch node - currently not used
  """
  def __init__(self, kwargs):
    """
    :param kwargs:
    """
    super().__init__(**kwargs)
    self.__dict__.update(locals())
    del self.self
    self.commits = []

  def add_commit(self, commit):
    """
    :param commit
    """
    self.commits.append(commit)


class Commit(CustomNode):
  """Commit OGM  - Mapps Commit from PyDriller to py2neo
  """
  def __init__(self, commit, graph=None, repo=None):
    """Instantiates a commit. If a graph is given
    the node is created in the graph
    :param commit: pydriller Commit object
    :param graph: py2neo Graph object
    :param repo: pydriller RepositoryMining object
    """
    self.node_type="Commit"
    self.node_index = "hash"

    self.commit = commit
    self.indexed = False
    CustomNode.__init__(self, self.node_type, hash=self.commit.hash)

    if graph is not None:
      self.index_all(graph=graph, repo=repo)

  def index_files_changed(self, graph):
    """Indexes the files changed by a commit
    :param graph: py2neo graph object
    """
    self.check_self(graph)
    for chg in self.commit.modifications:
      change = File(chg, graph=graph)
      rel.File(rel_from=self, rel_to=change, graph=graph)

  def index_author(self, graph):
    """Indexes the commit author node in the graph
    and adds relationship to this commit
    :params graph: py2neo graph object
    """
    self.check_self(graph)
    dev = Developer(self.commit.author, graph=graph)
    rel.Authorship(dev, self, graph=graph)

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
      rel.Parent(commit, self, graph=graph)

  def index_date(self, graph):
    """Splits the date in year, month and day and creates
    the graph nodes and relationships
    :param graph: py2neo graph object
    """
    self.check_self(graph)

    date = self.commit.author_date
    day = Day(date, graph=graph)
    month = Month(date, graph=graph)
    year = Year(date, graph=graph)

    rel.YearMonth(year, month, graph=graph)
    rel.YearMonth(year, month, graph=graph)
    rel.MonthDay(month, day, graph=graph)
    rel.DayCommit(day, self, graph=graph)


  def index_all(self, graph, repo=None):
    """Indexes all the data for a commit
    :param graph: py2neo graph object
    :param repo: PyDriller RepositoryMining class for the
      current repo
    """
    self.check_self(graph)
    self.index_author(graph)
    self.index_date(graph)
    self.index_files_changed(graph)

    if repo is not None:
      self.index_parents(graph, repo)


class File(CustomNode):
  """File OGM Node - Maps files changed in a commit
  to py2neo objects
  """
  def __init__(self, file, graph=None, file_type=True):
    """Instantiates file object. If a graph is provided
    the node is also added to neo4j
    :param file: pydriller Modification object
    :param graph: py2neo graph object
    :param file_type: flag which decides if the file type
      should be indexed
    """
    self.node_type = "File"
    self.node_index = "hash"

    self.file = file
    _hash =  hashlib.sha224(str(file.filename).encode('utf-8')).hexdigest()
    super().__init__(self.node_type, hash=_hash, name=file.filename)
    if graph is not None:
      self.index(graph)

  def index(self, graph):
    """Adds node in the graph
    :param graph: py2neo graph
    """
    graph.merge(self, self.node_type, self.node_index)

  def index_type(self):
    """Creates file type if it does not exist and adds filetype
    relationship"""
    pass

class Filetype(CustomNode):
  """Filetype OGM Node - Maps file types to py2neo object
  """
  def __init__(self, file, graph=None):
    """Instantiate Filetype object. If a graph is provided
    the node is also added to neo4j
    :param file: pydriller Modification object
    :param graph: py2neo graph object
    """
    self.node_type = "Filetype"
    self.node_index = "hash"

    _name = file.filename.split()[-1:]
    _hash = hashlib.sha224(_name).hexdigest()
    super().__init__(self.node_type, hash=_hash, name=_name)
    if graph is not None:
      self.index(graph)

  def index(self, graph):
    """Adds file type node in the graph
    :param graph: py2neo graph object
    """
    graph.merge(self, self.node_type, self.node_index)


class Developer(CustomNode):
  """Developer OGM Node - Maps PyDriller Developer objects
  to py2neo. Should be changed to Contributor in the future
  """

  def __init__(self, actor, graph=None):
    """Instantiates a developer object. If a graph is provided
    the object is indexed in neo4j
    :param actor: pydriller Actor object
    :param graph: py2neo graph
    """
    self.node_type = "Developer"
    self.node_index = "email"

    self.actor = actor
    super().__init__(self.node_type, name=self.actor.name, email=self.actor.email)
    if graph is not None:
      self.index(graph)

  def index(self, graph):
    """Adds graph node for this object
    :param graph: py2neo graph
    """
    graph.merge(self, self.node_type, self.node_index)


class Year(CustomNode):
  """Year OGM node
  """
  def __init__(self, date, graph=None):
    """Instantiates a year object. If a graph is provided
    the object is indexed in neo4j
    :param date: datetime object containing all date info
    """
    self.node_type = "Year"
    self.node_index = "name"

    super().__init__(self.node_type, name=date.year)
    if graph is not None:
      self.index(graph)

  def index(self, graph):
    """Adds graph node for this object
    :param graph: py2neo graph
    """
    graph.merge(self, self.node_type, self.node_index)

class Month(CustomNode):
  """Month node
  """
  def __init__(self, date, graph=None):
    """Instantiates a month object and creates an unique
    hash for each month of each year. This model was chosen
    because we aim to represent time series. If a graph is
    provided the object is indexed in neo4j
    :param date: datetime object containing all date info
    """
    self.node_type = "Month"
    self.node_index = "hash"

    _hash = hashlib.sha224((str(date.month) + str(date.year)).encode('utf-8')).hexdigest()
    super().__init__(self.node_type, name=date.month, hash=_hash)
    if graph is not None:
      self.index(graph)

  def index(self, graph):
    """Adds graph node for this object
    :param graph: py2neo graph
    """
    graph.merge(self, self.node_type, self.node_index)

class Day(CustomNode):
  """Day node
  """
  def __init__(self, date, graph=None):
    """Instantiates a day object and hashes the month, year and
    day as an unique key for the day. We wish to simulate a time
    series (otherwise, each month could've connect to the same day).
    If a graph is provided, the object is indexed in neo4j
    :param date: datetime object containing all date info
    """
    self.node_type = "Day"
    self.node_index = "hash"

    _hash = hashlib.sha224((str(date.month) + str(date.year) + str(date.day)).encode('utf-8')).hexdigest()
    super().__init__("Day", name=date.day, hash=_hash)
    if graph is not None:
      self.index(graph)

  def index(self, graph):
    """Adds graph node for this object
    :param graph: py2neo graph
    """
    graph.merge(self, self.node_type, self.node_index)
