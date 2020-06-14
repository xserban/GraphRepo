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
"""This module mines commits and contains all related Neo4j queries"""

from graphrepo.miners.default import DefaultMiner
from graphrepo.miners.utils import format_commit_id_date


class CommitMiner(DefaultMiner):
    """This class holds queries for commits"""

    def query(self, **kwargs):
        """Queries commits by any arguments given in kwargs
        For example kwargs can be {'hash': 'example-hash'}
        :param kwargs: any parameter and value, between hash, name or email
        :returns: list of commit nodes matched
        """
        com_ = self.node_matcher.match("Commit", **kwargs)
        return [dict(x) for x in com_]

    def get_between_dates(self, start_date, end_date,
                          project_id=None):
        """Returns all commits between start and end date
        :param start_date: timestamp, start date
        :param end_date: timestamp, end date
        :param project_id: optional; if given only the commits from a project
          are returned
        :returns: list of commitss
        """
        com_filter, where = format_commit_id_date(
            project_id, start_date, end_date)
        query = """
        MATCH (c: Commit {0})
        {1}
        RETURN distinct c
        """.format(com_filter, where)
        dt_ = self.graph.run(query)
        return [dict(x['c']) for x in dt_.data()]

    def get_all(self,):
        """Returns all commits
        :returns: list of commit nodes
        """
        com_ = self.node_matcher.match("Commit")
        return [dict(x) for x in com_]

    def get_commit_files(self, commit_hash):
        """Returns the files updated in a commit
        :param commit_hash: optional; if given, it will
          return the data only for one commit
        :returns: list of commit files
        """
        query = """
          MATCH (c:Commit {{hash: "{0}"}})
          -[UpdateFile]->(f:File)
          return distinct f
          """.format(commit_hash)
        files_ = self.graph.run(query)
        return [x['f'] for x in files_.data()]

    def get_commit_file_updates(self, commit_hash):
        """Returns the updates a commit made to files (UpdateFile rel)
        :param commit_hash: optional; if given, it will
          return the data only for one commit
        :returns: list of
        """
        query = """
          MATCH (c:Commit {{hash: "{0}"}})
          -[f: UpdateFile]->(fu:File)
          return distinct f
          """.format(commit_hash)
        files_ = self.graph.run(query)
        return [x['f'] for x in files_.data()]

    def get_commit_methods(self, commit_hash=None):
        """Returns the methods updated in a commit
        :param commit_hash: optional; if given, it will
          return the data only for one commit
        """
        query = """
          MATCH (c:Commit {{hash: "{0}"}})
          -[UpdateMethod]->(m:Method)
          return distinct m
          """.format(commit_hash)
        files_ = self.graph.run(query)
        return [x['m'] for x in files_.data()]

    def get_commit_method_updates(self, commit_hash=None):
        """Returns the updatemethod relationships from a commit
        :param commit_hash: optional; if given,
          it will return the data only for one commit
        :param dic: optional, boolean for ocnverting the data to dictionaries
        """
        query = """
          MATCH (c:Commit {{hash: "{0}"}})
          -[m:UpdateMethod]->(mu:Method)
          return distinct m
          """.format(commit_hash)
        files_ = self.graph.run(query)
        return [x['m'] for x in files_.data()]
