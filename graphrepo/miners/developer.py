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
"""This module mines developers and contains all related Neo4j queries"""

from graphrepo.miners.default import DefaultMiner


class DeveloperMiner(DefaultMiner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def query(self, **kwargs):
        """Queries developers by any arguments given in kwargs
        For example kwargs can be {'hash': 'example-hash'} or
        {'email': 'example-email'}
        :param kwargs: any parameter and value, between hash, name or email
        :returns: list of nodes matched
        """
        return list(self.node_matcher.match("Developer", **kwargs))

    def get_commits(self, dev_hash, project_id=None):
        """Returns all commits authored by a developer.
        Optionally, it also filters by project id
        :param dev_hash: developer unique identifier
        :param project_id: optional; if present the
          query returns the commits from a project
        :returns: list of commits
        """
        if project_id:
            query = """
            MATCH (d:Developer {{hash: "{0}"}})
                  -[r:Author]->
                  (c:Commit {{project_id: "{1}"}})
            RETURN c;
          """.format(dev_hash, project_id)
        else:
            query = """
            MATCH (d:Developer {{hash: "{0}"}})
                  -[r:Author]->
                  (c:Commit)
            RETURN c;
          """.format(dev_hash)

        return list(self.graph.run(query))

    def get_files(self, dev_hash, project_id=None):
        """Returns all files edited by a developer.
        Optionally it also filters by project_id
        :params dev_hash: developer unique identifier
        :params project_id: optional; if present the query
          returns the files from a specific project
        """
        if project_id:
            query = """
            MATCH (d:Developer {{hash: "{0}"}})
                  -[r:Author]->
                  (c:Commit {{project_id: "{1}"}})
                  -[UpdateFile]->
                  (f: File)
            RETURN collect(distinct f);
          """.format(dev_hash, project_id)
        else:
            query = """
            MATCH (d:Developer {{hash: "{0}"}})
                  -[r:Author]->
                  (c:Commit)
                  -[UpdateFile]->
                  (f: File)
            RETURN collect(distinct f);
          """.format(dev_hash, project_id)
        files = self.graph.run(query).data()[
            0]['collect(distinct f)']  # here we transform the aggregation back to a list
        return [dict(x) for x in files]  # map to list of dictionaries

    def get_files_updates(self, dev_hash, project_id=None):
        """Returns all files, together with the update
        information (e.g. file complexity), for all files
        edited by a developer.
        Optionally it also filters by project_id
        :params dev_hash: developer unique identifier
        :params project_id: optional; if present the query
          returns the files from a specific project
        """
        if project_id:
            query = """
          MATCH (d:Developer {{hash: "{0}"}})
                -[r:Author]->
                (c:Commit {{project_id: "{1}"}})
                - [fu: UpdateFile] ->
                (f: File)
          RETURN fu;
        """.format(dev_hash, project_id)
        else:
            query = """
          MATCH (d:Developer {{hash: "{0}"}})
                -[r:Author]->
                (c:Commit)
                - [fu: UpdateFile] ->
                (f: File)
          RETURN fu;
        """.format(dev_hash, project_id)
        updates = [dict(x) for x in self.graph.run(query).data()]  # .data()
        print(updates[0])
        return updates

    def get_methods():
        pass

    def get_methods():
        pass

    def get_all(self):
        return self.node_matcher.match("Developer")
