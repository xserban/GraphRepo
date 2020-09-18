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
from graphrepo.miners.utils import format_commit_id_date as fcid


class DeveloperMiner(DefaultMiner):
    """This class holds queries for the Developer nodes"""

    def query(self, **kwargs):
        """Queries developers by any arguments given in kwargs
        For example kwargs can be {'hash': 'example-hash'} or
        {'email': 'example-email'}
        :param kwargs: any parameter and value, between hash, name or email
        :returns: list of nodes matched
        """
        return self.node_matcher.match("Developer", **kwargs)

    def get_commits(self, dev_hash, project_id=None,
                    start_date=None, end_date=None):
        """Returns all commits authored by a developer.
        Optionally, it also filters by project id
        :param dev_hash: developer unique identifier
        :param project_id: optional; if present the
          query returns the commits from a project
        :param start_date: optional timestamp; filter commits
          beginning with this date
        :param end_date: optional timestamp; filter commits
          untill this date
        :returns: list of commits
        """
        com_filter, where = fcid(project_id,
                                 start_date, end_date)
        cquery = """
        MATCH (d:Developer {{hash: "{0}"}})
              -[r:Author]->
              (c:Commit {1})
        {2}
        RETURN distinct c;
        """.format(dev_hash, com_filter, where)
        dt_ = self.graph.run(cquery)
        return [dict(x['c']) for x in dt_.data()]

    def get_files(self, dev_hash, project_id=None,
                  start_date=None, end_date=None):
        """Returns all files edited by a developer.
        Optionally it also filters by project_id
        :params dev_hash: developer unique identifier
        :params project_id: optional; if present the query
          returns the files from a specific project
        :param start_date: optional timestamp; filter files
          beginning with this date
        :param end_date: optional timestamp; filter files
          untill this date
        :returns: list of files
        """
        com_filter, where = fcid(project_id,
                                 start_date, end_date)
        fquery = """
        MATCH (d:Developer {{hash: "{0}"}})
              -[r:Author]->
              (c:Commit {1})
              -[UpdateFile]->
              (f: File)
        {2}
        RETURN collect(distinct f);
        """.format(dev_hash, com_filter, where)
        dt_ = self.graph.run(fquery)
        return [dict(x) for x in dt_.data()[0]['collect(distinct f)']]

    def get_files_updates(self, dev_hash, project_id=None,
                          start_date=None, end_date=None):
        """Returns all file update information (e.g. file complexity),
        for all files edited by a developer.
        Optionally it also filters by project_id
        :params dev_hash: developer unique identifier
        :params project_id: optional; if present the query
          returns the files from a specific project
        :param start_date: optional timestamp; filter files
          beginning with this date
        :param end_date: optional timestamp; filter files
          untill this date
        :returns: list of file updates
        """
        com_filter, where = fcid(project_id,
                                 start_date, end_date)
        fuquery = """
        MATCH (d:Developer {{hash: "{0}"}})
              -[r:Author]->
              (c:Commit {1})
              -[fu: UpdateFile]->
              (f: File)
        {2}
        RETURN distinct fu;
        """.format(dev_hash, com_filter, where)

        dt_ = self.graph.run(fuquery)
        return [dict(x['fu']) for x in dt_.data()]

    def get_methods(self, dev_hash, project_id=None,
                    start_date=None, end_date=None):
        """Returns all methods updated by a developer.
        Optionally it also filters by project_id
        :params dev_hash: developer unique identifier
        :params project_id: optional; if present the query
          returns the files from a specific project
        :param start_date: optional timestamp; filter files
          beginning with this date
        :param end_date: optional timestamp; filter files
          untill this date
        :returns: list of methods
        """
        com_filter, where = fcid(project_id,
                                 start_date, end_date)
        mquery = """
        MATCH (d:Developer {{hash: "{0}"}})
              -[r:Author]->
              (c:Commit {1})
              -[um: UpdateMethod]->
              (m: Method)
        {2}
        RETURN distinct m;
        """.format(dev_hash, com_filter, where)

        dt_ = self.graph.run(mquery)
        return [dict(x['m']) for x in dt_.data()]

    def get_method_updates(self, dev_hash, project_id=None,
                           start_date=None, end_date=None):
        """Returns all method update information, for all
        methods update by a developer.
        Optionally it also filters by project_id
        :params dev_hash: developer unique identifier
        :params project_id: optional; if present the query
          returns the files from a specific project
        :param start_date: optional timestamp; filter files
          beginning with this date
        :param end_date: optional timestamp; filter files
          untill this date
        :returns: list of method updates
        """
        com_filter, where = fcid(project_id,
                                 start_date, end_date)
        muquery = """
        MATCH (d:Developer {{hash: "{0}"}})
              -[r:Author]->
              (c:Commit {1})
              -[um: UpdateMethod]->
              ()
        {2}
        RETURN distinct um;
        """.format(dev_hash, com_filter, where)

        dt_ = self.graph.run(muquery)
        return [dict(x['um']) for x in dt_.data()]

    def get_all(self):
        return self.node_matcher.match("Developer")
