
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
"""Default Parent class for drillers
"""
from abc import abstractmethod
from datetime import datetime
from py2neo import Graph
from pydriller import RepositoryMining

import graphrepo.utils as utl
import graphrepo.drillers.db_init as db_init
from graphrepo.config import Config
from graphrepo.logger import Logger
LG = Logger()


class DefaultDriller():
    """DefaultDriller class - parses a git repo and uses the models
    to index everything in Neo4j.
    """

    def __init__(self, config_path):
        """Initializes the properties of this class
        :param config_path: path to yml config file
        """
        try:
            if not config_path:
                raise FileNotFoundError
            neo, project = utl.parse_config(config_path)
            self.config = Config()
            self.graph = None
            self.config.configure(**neo, **project)
            self._connect()
        except Exception as exc:
            LG.log_and_raise(exc)

    def _connect(self):
        """Instantiates the connection to Neo4j and stores
        the graph internally.
        Throws exception if the connection can not pe realized
        """
        try:
            self.graph = Graph(host=self.config.ct.db_url,
                               user=self.config.ct.db_user,
                               password=self.config.ct.db_pwd,
                               port=self.config.ct.port)
        except Exception as exc:
            LG.log_and_raise(exc)

    def _check_connection(self):
        """Checks if there is a db connection and raises
        ReferenceError if not.
        """
        try:
            self._connect()
        except:
            raise ReferenceError("There is no valid "
                                 "database connection. Please "
                                 "configure and connect first.")

    def init_db(self):
        """Runs initialization of a database; creates
        constraints and indexes"""
        try:
            self._check_connection()
            db_init.create_hash_constraints(self.graph)
            db_init.create_indices(self.graph, hash_index=False)
        except Exception as e:
            raise e

    def clean(self):
        """Removes all data in a graph
        """
        try:
            self.config.check_config()
            self._check_connection()

            self.graph.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")
        except Exception as exc:
            LG.log_and_raise(exc)

    def drill_batch(self, index=True, save_path=None):
        """Extracts data from a software repository, with the option
        of saving it on diks and indexing it in Neo4j
        :param index: optional, if True, the data is indexed in Neo4j
        :param save_path: optional, if given, the data is stored on dik
        :returns: dictionary with all data
        """
        start = datetime.now()
        print('Driller started at: \t', start)
        commits, parents, devs, dev_com, branches,\
            branches_com, files, com_files, \
            methods, files_methods, com_methods = \
            [], [], [], [], [], [], [], [], [], [], []
        for commit in \
            RepositoryMining(self.config.ct.repo,
                             since=self.config.ct.start_date,
                             to=self.config.ct.end_date).traverse_commits():
            self.drill_commit(commit, commits, parents, devs, dev_com, branches,
                              branches_com, files, com_files,
                              methods, files_methods, com_methods)

        data_ = self.data_dot_dict(commits, parents, devs, dev_com, branches,
                                   branches_com, files, com_files,
                                   methods, files_methods, com_methods)

        print('Driller finished in: \t', datetime.now() - start)

        if save_path:
            utl.save_json(save_path, data_)
        if index:
            self.index_batch(**data_)
        return data_

    def drill_commit(self, commit, commits, parents, devs, dev_com, branches,
                     branches_com, files, com_files,
                     methods, files_methods, com_methods):
        """Helper method - works with pass by reference"""
        timestamp = commit.author_date.timestamp()
        dev = utl.format_dev(commit, self.config.ct.index_developer_email)
        devs.append(dev)
        com = utl.format_commit(commit, self.config.ct.project_id)
        commits.append(com)
        dev_com.append(utl.format_author_commit(dev, com, timestamp))
        for parent in commit.parents:
            parents.append(utl.format_parent_commit(
                com['hash'], parent, self.config.ct.project_id))
        for branch in commit.branches:
            br_ = utl.format_branch(branch, self.config.ct.project_id)
            branches.append(br_)
            branches_com.append(
                utl.format_branch_commit(br_['hash'], com['hash']))
        for file in commit.modifications:
            fl_ = utl.format_file(file, self.config.ct.project_id)
            files.append(fl_)
            com_files.append(utl.format_commit_file(
                com['hash'], fl_['hash'], file,
                timestamp, self.config.ct.index_code))
            for method in file.changed_methods:
                met = utl.format_method(
                    method, file, self.config.ct.project_id)
                methods.append(met)
                files_methods.append(
                    utl.format_file_method(fl_['hash'], met['hash'])
                )
                com_methods.append(
                    utl.format_commit_method(com['hash'], met['hash'],
                                             method, timestamp))

    def data_dot_dict(self, commits, parents, devs, dev_com, branches,
                      branches_com, files, com_files,
                      methods, files_methods, com_methods):
        """Helper method"""
        return utl.Dotdict({'commits': commits,
                            'parents': parents,
                            'developers': devs,
                            'dev_commits': dev_com,
                            'branches': branches,
                            'branches_commits': branches_com,
                            'files': files,
                            'commit_files': com_files,
                            'methods': methods,
                            'file_methods': files_methods,
                            'commit_methods': com_methods})

    @abstractmethod
    def index_batch(self):
        """Abstract index batch driller method
        """
        raise NotImplementedError
