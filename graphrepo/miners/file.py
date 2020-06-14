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
    """This clas holds queries for the File nodes"""

    def query(self, **kwargs):
        """Searches for a file using the arguments in kwargs.
        If no kwargs are given it returns the first file found
        """
        return self.node_matcher.match("File", **kwargs).first()

    def get_all(self):
        """Returns all node of type File
        :return: list of files
        """
        return self.node_matcher.match("File")

    def get_change_history(self, file_hash):
        """Returns all updated relationships
        :param file_hash: a string, unique identifier for file
        :param dic: optional; boolean for converting data to dictionary
          or returning it as py2neo records - the py2neo raw
          records can be used in mappers
        :return: list of update file relationships
        """
        query = """MATCH ()-[r:UpdateFile]->(f:File {{hash: "{0}"}})
        return distinct r
        """.format(file_hash)
        dt_ = self.graph.run(query)
        return [dict(x['r']) for x in dt_.data()]

    def get_current_methods(self, file_hash):
        """Returns all current methods
        :param file_hash: a string, unique identifier for file
        :param dic: optional; boolean for converting data to dictionary
          or returning it as py2neo records - the py2neo raw
          records can be used in mappers
        :return: list of methods
        """
        query = """MATCH (f:File {{hash: "{0}"}})-[r:Method]->(m:Method)
        return distinct m
        """.format(file_hash)
        dt_ = self.graph.run(query)
        return [dict(x['m']) for x in dt_.data()]

    def get_past_methods(self, file):
        """Returns methods that were removed from the file
          :param file: Py2Neo File object
          :returrn: list of Method objects
          """
        # return [rel.end_node
        #         for rel in self.graph.match([file, None], "HadMethod")]
