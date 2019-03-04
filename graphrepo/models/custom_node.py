"""This module represents a custom py2neo Node which
should be inherited by all models
"""
from py2neo.data import Node

class CustomNode(Node):
  """Parent class for all custom Nodes"""
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