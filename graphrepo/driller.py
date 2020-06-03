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
import graphrepo.utils as utl
import graphrepo.batch_utils as b_utl
from py2neo import Graph, NodeMatcher
from pydriller import RepositoryMining, GitRepository
from graphrepo.config import Config
from graphrepo.logger import Logger
from graphrepo.models.commit import Commit
from graphrepo.singleton import Singleton
from datetime import datetime
LG = Logger()


class Driller(metaclass=Singleton):
    """Drill class - parses a git repo and uses the models
    to index everything in Neo4j. This class is a singleton
    because it holds the connection to Neo4j in self.graph
    """

    def __init__(self, *args, **kwargs):
        """Initializes the properties of this class"""
        self.config = Config()
        self.graph = None
        self.configure(*args, **kwargs)

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
        self.config.BATCH_SIZE = kwargs['batch_size']

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

    def drill_batch(self, index=True):
        start = datetime.now()
        print('Driller started at: \t', start)
        commits, devs, dev_com, branches, branches_com, files, com_files, \
            methods, files_methods, com_methods = [], [], [], [], [], [], [], [], [], []
        for commit in RepositoryMining(self.config.REPO,
                                       since=self.config.START_DATE,
                                       to=self.config.END_DATE).traverse_commits():
            timestamp = commit.author_date.timestamp()
            dev = utl.format_dev(commit)
            devs.append(dev)
            com = utl.format_commit(commit, self.config.PROJECT_ID)
            commits.append(com)
            dev_com.append(utl.format_author_commit(dev, com, timestamp))
            for branch in commit.branches:
                br_ = utl.format_branch(branch, self.config.PROJECT_ID)
                branches.append(br_)
                branches_com.append(
                    utl.format_branch_commit(br_['hash'], com['hash']))
            for file in commit.modifications:
                fl = utl.format_file(file, self.config.PROJECT_ID)
                files.append(fl)
                com_files.append(utl.format_commit_file(
                    com['hash'], fl['hash'], file, timestamp))
                for method in file.changed_methods:
                    met = utl.format_method(
                        method, file, self.config.PROJECT_ID)
                    methods.append(met)
                    files_methods.append(
                        utl.format_file_method(fl['hash'], met['hash'])
                    )
                    com_methods.append(utl.format_commit_method(com['hash'],
                                                                met['hash'], method, timestamp))
        data_ = {'commits': commits,
                 'developers': devs,
                 'dev_commits': dev_com,
                 'branches': branches,
                 'branches_commits': branches_com,
                 'files': files,
                 'commit_files': com_files,
                 'methods': methods,
                 'file_methods': files_methods,
                 'commit_methods': com_methods}
        print('Driller finished at: \t', datetime.now() - start)
        if index:
            self.index_batch(**data_)
        return data_

    def index_batch(self, *args, **kwargs):
        try:
            self.config.check_config()
            self.check_connection()
            b_utl.index_all(
                self.graph, batch_size=self.config.BATCH_SIZE,  **kwargs)
        except Exception as exc:
            LG.log_and_raise(exc)
        else:
            return

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
