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
        return self.node_matcher.match("Method")

    def get_change_history(self, method_hash):
        """Returns all UpdateMethod relationships
          :param method_hash: method unique identifier
          :param dic: optional; boolean for converting data to dictionary
          or returning it as py2neo records - the py2neo raw
          records can be used in mappers
          :return: list of UpdateMethod relationships / dics
          """
        query = """MATCH ()-[r:UpdateMethod]->(m: Method{{hash: "{0}"}})
        RETURN distinct r
          """.format(method_hash)
        dt_ = self.graph.run(query)
        return [dict(x['r']) for x in dt_.data()]
