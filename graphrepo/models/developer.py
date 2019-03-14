# Copyright 2019 NullConvergence
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
