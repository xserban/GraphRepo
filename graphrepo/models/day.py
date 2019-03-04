"""This module is a mapping to a neo4j node for a day"""
import hashlib

from graphrepo.models.custom_node import CustomNode

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