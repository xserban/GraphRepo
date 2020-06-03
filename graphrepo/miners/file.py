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


class FileMiner(DefaultMiner):
    def __init__(self, graph, node_matcher, rel_matcher, *args, **kwargs):
        super().__init__(graph, node_matcher, rel_matcher, *args, **kwargs)

    def query(self, **kwargs):
        """Searches for a file using the arguments in kwargs.
        If no kwargs are given it returns the first file found
        """
        return self.node_matcher.match("File", **kwargs).first()

    def get_all(self):
        """Returns all node of type File
        :return: list of files
        """
        return list(self.node_matcher.match("File"))

    def get_change_history(self, file):
        """Returns all updated relationships
        :param file: a Py2Neo File object
        :return: list of update file relationships
        """
        return list(self.rel_matcher.match([None, file], "UpdateFile"))

    def get_current_methods(self, file):
        """Returns all current methods
        :param file: Py2Neo File object
        :returrn: list of Method objects
        """
        return [rel.end_node
                for rel in self.graph.match([file, None], "Method")]

    def get_past_methods(self, file):
        """Returns methods that were removed from the file
          :param file: Py2Neo File object
          :returrn: list of Method objects
          """
        # return [rel.end_node
        #         for rel in self.graph.match([file, None], "HadMethod")]
        pass
