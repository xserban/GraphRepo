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

"""This module is a mapping to a neo4j node for a day"""

from graphrepo.models.custom_node import CustomNode


class Branch(CustomNode):
  """Branch node
  """

  def __init__(self, name, project_id=None, graph=None, *args, **kwargs):
    """Instantiates a branch node and, if a graph is given,
    it indexes the graph to Neo4j
    :param name: string containing an unique name
    :param project_id: a string identifying the project a branch belogns to
    :param graph: py2neo graph objects
    """
    self.node_type = "Branch"
    self.node_index = "name"

    super().__init__(self.node_type, name=name,
                     project_id=project_id, *args, **kwargs)
    if graph is not None:
      self.index(graph)
