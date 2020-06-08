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
from diskcache import Cache
from datetime import datetime
from py2neo import Graph
from pydriller import RepositoryMining

import graphrepo.utils as utl
import graphrepo.drillers.batch_utils as b_utl
from graphrepo.config import Config
from graphrepo.drillers.drill_cache import DrillCacheSequential
from graphrepo.drillers.default import DefaultDriller
from graphrepo.logger import Logger

LG = Logger()


class Driller(DefaultDriller):
    """Drill class - parses a git repo and uses the models
    to index everything in Neo4j. This class is a singleton
    because it holds the connection to Neo4j in self.graph
    """

    def index_batch(self, **kwargs):
        """Indexes data extracted by drill_batch of from
        disk in Neo4j
        :param kwargs: data keys and values (see the drill_batch return)
        """
        try:
            self.config.check_config()
            self._check_connection()
            b_utl.index_all(
                self.graph, batch_size=self.config.ct.batch_size, **kwargs)
        except Exception as exc:
            LG.log_and_raise(exc)
        else:
            return

    def index_from_file(self, file_path):
        """Reads a file and indexes the data in Neo4j
        :param file_path: the path of the JSON file with data
        """
        try:
            data_ = utl.load_json(file_path)
            self.index_batch(**data_)
        except Exception as exc:
            LG.log_and_raise(exc)
        else:
            return
