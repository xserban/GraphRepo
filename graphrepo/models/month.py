"""This module is a mapping to a neo4j node for a month"""
import hashlib

from graphrepo.models.custom_node import CustomNode

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
