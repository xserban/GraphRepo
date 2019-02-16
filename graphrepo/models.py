""" Thsi modules Defines all neo4j ORM models
"""
from py2neo.data import Node
import relationships as rl

class Branch(Node):
  """ Branch node - might not be needed
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
  """ Commit node
  """

  def __init__(self, commit):
    """
    :param commit
    """
    self.commit = commit
    self.changes = []
    self.indexed = False
    Node.__init__(self, "Commit", hash=self.commit.hash)

  def _get_changes(self):
    """
    """
    if len(self.changes) < 0:
      for chg in self.commit.modifications:
        self.changes.append(Change(chg))
    return self.changes

  def index_author(self, graph):
    self.check_self(graph)
    dev = Developer(self.commit.author)
    graph.merge(dev, "Developer", "email")
    rel = rl.Authorship(dev, self)
    graph.create(rel)

  def index_parents(self, graph, repo):
    self.check_self(graph)
    for parent in self.commit.parents:
      commit = Commit(repo.get_commit(parent))
      commit.index_author(graph)
      rel = rl.Parent(commit, self)
      graph.create(rel)


  def check_self(self, graph):
    if not self.indexed:
      graph.merge(self, "Commit", "hash")

  def index_all(self, graph, repo):
    self.check_self(graph)
    self.index_author(graph)
    self.index_parents(graph, repo)


class Change(Node):
  """ Change node - for files changed in a commit
  """

  def __init__(self, change):
    """
    :param change
    """
    self.change = change
    Node.__init__(self, "Change")



class Developer(Node):
  """ Developer node - for any person involved in
  a project. Can be changed to contributor in the future
  """

  def __init__(self, actor):
    """
    :param actor
    """
    self.actor = actor
    Node.__init__(self, "Developer",  name=self.actor.name, email=self.actor.email)

