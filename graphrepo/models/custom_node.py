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

    def index(self, graph):
        """Adds graph node for this object
        :param graph: py2neo graph
        """
        graph.merge(self, self.node_type, self.node_index)
