"""This module is a mapping to a neo4j node for a year"""
import hashlib

from graphrepo.models.custom_node import CustomNode

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