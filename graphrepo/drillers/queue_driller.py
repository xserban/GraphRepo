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
from graphrepo.drillers.driller import Driller
import graphrepo.drillers.batch_utils as b_utl
from graphrepo.logger import Logger

LG = Logger()


class QueueDriller(Driller):
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

    @abstractmethod
    def connect_queue(self):
        """Establishes a connection to queue"""
        raise NotImplementedError

    @abstractmethod
    def send_index_data(self, data):
        """Indexes data"""
        raise NotImplementedError

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

            self.drill_commit(commit, commits, parents, devs, dev_com, branches,
                              branches_com, files, com_files,
                              methods, files_methods, com_methods)

            if commit_index == self.queue['commit_batch'] - 1:
                data_ = self.data_dot_dict(commits, parents, devs, dev_com, branches,
                                           branches_com, files, com_files,
                                           methods, files_methods, com_methods)

                self.send_index_data(
                    {'project_conf': self.project, 'data': data_})

                commits, parents, devs, dev_com, branches, branches_com, files, com_files, methods, files_methods, com_methods = [
                ], [], [], [], [], [], [], [], [], [], []
                commit_index = 0
            else:
                commit_index += 1

        print('Driller finished in: \t', datetime.now() - start)
