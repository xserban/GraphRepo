
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
from graphrepo.config import Config
from graphrepo.drillers.default import DefaultDriller
import graphrepo.drillers.batch_utils as b_utl
from graphrepo.logger import Logger

LG = Logger()


class QueueDriller(DefaultDriller):
    """QueueDriller class - parses a git repo and publishes
    the data in a queue every n commits
    """

    def __init__(self, neo, project, queue):
        """Initializes the properties of this class
        :param neo:
        :param project:
        :param queue:
        """
        # TODO: validate inputs
        try:
            self.project, self.queue = project, queue
            self.config = Config()
            self.graph = None
            self.config.configure(**neo, **self.project)
            # self._connect()
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
        commit_index = 0
        for commit in \
            RepositoryMining(self.config.ct.repo,
                             since=self.config.ct.start_date,
                             to=self.config.ct.end_date).traverse_commits():

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

            if commit_index == self.queue['commit_batch'] - 1:
                data_ = utl.Dotdict({'commits': commits,
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

                self.send_index_data(
                    {'project_conf': self.project, 'data': data_})

                commits, parents, devs, dev_com, branches, branches_com, files, com_files, methods, files_methods, com_methods = [
                ], [], [], [], [], [], [], [], [], [], []
                commit_index = 0
            else:
                commit_index += 1

        print('Driller finished in: \t', datetime.now() - start)

    @abstractmethod
    def connect_queue(self):
        """Establishes a connection to queue"""
        raise NotImplementedError

    @abstractmethod
    def send_index_data(self, data):
        """Indexes data"""
        raise NotImplementedError
