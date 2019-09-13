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

"""This module is a mapping to a neo4j node for a method"""
import hashlib

from graphrepo.models.custom_node import CustomNode


class Method(CustomNode):
  """Method node
  """

  def __init__(self, method, graph=None):
    """Instantiates a method object and creates an unique
    hash
    :param method: PyDriller Method object
    """
    self.node_type = "Method"
    self.node_index = "name"

    self.method = method
    super().__init__(self.node_type, name=self.method.name)
    if graph is not None:
      self.index(graph)
