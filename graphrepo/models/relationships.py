"""This module holds all possible relationships in the graph"""
from py2neo.data import Relationship

class CustomRelationship(Relationship):
  """Extends py2neo relationship object
  with custom functionality.
  """
  def __init__(self, rel_from=None, rel_to=None, graph=None):
    """Instantiates a custom relationship. If a graph is given
    the relationship is indexed in the graph.
    :param rel_from: py2neo Node object
    :param rel_to: py2neo Node object
    :param graph: py2neo graph object
    """
    super().__init__(rel_from, rel_to)
    if graph is not None:
      self.create(graph)

  def create(self, graph):
    graph.create(self)


class Branch(CustomRelationship): pass
class Authorship(CustomRelationship): pass
class Parent(CustomRelationship): pass

class YearMonth(CustomRelationship): pass
class MonthDay(CustomRelationship): pass
class DayCommit(CustomRelationship): pass

class Branch(CustomRelationship): pass

class File(CustomRelationship): pass
class Filetype(CustomRelationship): pass