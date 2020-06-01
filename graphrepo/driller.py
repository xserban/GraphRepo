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

""" This module uses pydriller to search a repository
and indexes it in neo4j
"""
from py2neo import Graph, NodeMatcher
from pydriller import RepositoryMining, GitRepository
from graphrepo.config import Config
from graphrepo.logger import Logger
from graphrepo.models.commit import Commit
from graphrepo.singleton import Singleton


LG = Logger()


class Driller(metaclass=Singleton):
    """Drill class - parses a git repo and uses the models
    to index everything in Neo4j. This class is a singleton
    because it holds the connection to Neo4j in self.graph
    """

    def __init__(self):
        """Initializes the properties of this class"""
        self.config = Config()
        self.graph = None

    def configure(self, *args, **kwargs):
        """Sets the application constants"""
        # TODO: validate inputs
        self.config.DB_URL = kwargs['db_url']
        self.config.PORT = kwargs['port']
        self.config.DB_USER = kwargs['db_user']
        self.config.DB_PWD = kwargs['db_pwd']
        self.config.REPO = kwargs['repo']
        self.config.START_DATE = kwargs['start_date']
        self.config.END_DATE = kwargs['end_date']
        self.config.PROJECT_ID = kwargs['project_id']
        self.config.INDEX_DATE_NODES = kwargs['index_date_nodes']

    def connect(self):
        """Instantiates the connection to Neo4j and stores
        the graph internally.
        Throws exception if the connection can not pe realized
        """
        try:
            self.graph = Graph(host=self.config.DB_URL,
                               user=self.config.DB_USER,
                               password=self.config.DB_PWD,
                               port=self.config.PORT)
        except Exception as exc:
            LG.log_and_raise(exc)

    def _drill(self):
        """Parses all commits
        :returns: a tupple containing a list of commits and
          a Pydriller GitRepository commit
        """
        rep_obj = GitRepository(self.config.REPO)
        commits = []
        for commit in RepositoryMining(self.config.REPO,
                                       since=self.config.START_DATE,
                                       to=self.config.END_DATE).traverse_commits():
            commits.append(Commit(commit, self.config))

        return commits, rep_obj

    def drill(self):
        """Gets commits and indexes them to Neo4j Database"""
        try:
            self.config.check_config()
            self.check_connection()
            node_matcher = NodeMatcher(self.graph)

            commits, rep_obj = self._drill()
            for com in commits:
                com.index_all_data(self.graph, node_matcher, rep_obj)
        except Exception as exc:
            LG.log_and_raise(exc)
        else:
            return

    def check_connection(self):
        """Checks if there is a db connection and raises
        ReferenceError if not.
        """
        try:
            self.connect()
        except:
            raise ReferenceError("There is no valid "
                                 "database connection. Please "
                                 "configure and connect first.")

    def clean(self):
        """Removes all data in a graph
        """
        try:
            self.config.check_config()
            self.check_connection()

            self.graph.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")
        except Exception as exc:
            LG.log_and_raise(exc)
