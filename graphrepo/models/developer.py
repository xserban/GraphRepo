"""This module is a mapping from pydriller actor to a neo4j Developer node"""
import hashlib

from graphrepo.models.custom_node import CustomNode

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