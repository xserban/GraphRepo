# Copyright 2020 NullConvergence
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
"""This module mines files and contains all related Neo4j queries"""

from graphrepo.miners.default import DefaultMiner


class MethodMiner(DefaultMiner):
    def __init__(self, graph, node_matcher, rel_matcher, *args, **kwargs):
        super().__init__(graph, node_matcher, rel_matcher, *args, **kwargs)

    def query(self, **kwargs):
        """Searches for a method using the arguments in kwargs.
        If no kwargs are given it returns the first method found
        """
        return self.node_matcher.match("Method", **kwargs).first()

    def get_all(self):
        """Returns all node of type Method
        :return: list of method
        """
        return list(self.node_matcher.match("Method"))

    def get_change_history(self, method):
        """Returns all UpdateMethod relationships
          :param method: a Py2Neo Method Object
          :return: list of UpdateMethod relationships
          """
        return list(self.rel_matcher.match([None, method], "UpdateMethod"))