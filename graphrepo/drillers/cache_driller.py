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
from datetime import datetime
from pydriller import RepositoryMining

import graphrepo.utils as utl
import graphrepo.drillers.batch_utils as b_utl
from graphrepo.drillers.drill_cache import DrillCache, DrillCacheSequential
from graphrepo.drillers.default import DefaultDriller
from graphrepo.logger import Logger

LG = Logger()


class CacheDriller(DefaultDriller):
    """CacheDriller class - parses a git repo and uses the models
    to index everything in Neo4j by storing all data on disk.
    """

    def drill_batch_cache_sequential(self, index=True):
        """Extracts all information from a git repository
        and it stores in in a disk cache
        :param index: optional, if True, the data is indexed in Neo4j
        :returns: cache with all data
        """
        start = datetime.now()
        print('Driller started at: \t', start)
        cache = DrillCacheSequential()
        for commit in \
            RepositoryMining(self.config.ct.repo,
                             since=self.config.ct.start_date,
                             to=self.config.ct.end_date).traverse_commits():
            timestamp = commit.author_date.timestamp()
            dev = utl.format_dev(commit, self.config.ct.index_developer_email)
            cache.append_cache('developers', dev)
            com = utl.format_commit(commit, self.config.ct.project_id)
            cache.append_cache('commits', com)
            cache.append_cache(
                'dev_commits',
                utl.format_author_commit(dev, com, timestamp))
            for parent in commit.parents:
                cache.append_cache('parents', utl.format_parent_commit(
                    com['hash'], parent, self.config.ct.project_id))
            for branch in commit.branches:
                br_ = utl.format_branch(branch, self.config.ct.project_id)
                cache.append_cache('branches', br_)
                cache.append_cache('branches_commits', utl.format_branch_commit(
                    br_['hash'], com['hash']))
            for file in commit.modifications:
                fl_ = utl.format_file(file, self.config.ct.project_id)
                cache.append_cache('files', fl_)
                cache.append_cache('commit_files', utl.format_commit_file(
                    com['hash'], fl_['hash'], file, timestamp))
                for method in file.changed_methods:
                    met = utl.format_method(
                        method, file, self.config.ct.project_id)
                    cache.append_cache('methods', met)
                    cache.append_cache(
                        'file_methods',
                        utl.format_file_method(fl_['hash'],
                                               met['hash']))
                    cache.append_cache('commit_methods',
                                       utl.format_commit_method(
                                           com['hash'],
                                           met['hash'],
                                           method,
                                           timestamp))
        print('Driller finished in: \t', datetime.now() - start)
        if index:
            self.index_batch(cache)
        return cache

    def index_batch(self, cache):
        """Indexes cached data to Neo4j
        :param cache: diskcache Cache or Index
        """
        try:
            self.config.check_config()
            self._check_connection()
            b_utl.index_cache(
                self.graph, cache, batch_size=self.config.ct.batch_size)
        except Exception as exc:
            LG.log_and_raise(exc)
        else:
            return

    def drill_batch_cache_all(self, index=True):
        """Extracts the information from a repository in memory
        and caches it after the extraction
        :param index: optional, if True, the data is indexed in Neo4j
        """
        data = self.drill_batch(index=False)
        cache = DrillCache(data)
        if index:
            self.index_batch(cache)
        return cache
