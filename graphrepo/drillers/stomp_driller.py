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
import stomp
import json

from abc import abstractmethod
from datetime import datetime
from py2neo import Graph
from pydriller import RepositoryMining

import graphrepo.utils as utl
from graphrepo.config import Config
from graphrepo.drillers.queue_driller import QueueDriller
import graphrepo.drillers.batch_utils as b_utl
from graphrepo.logger import Logger

LG = Logger()


class StompDriller(QueueDriller):
    """StompDriller class - parses a git repo and publishes
    the data in a queue every n commits
    """

    def connect_queue(self):
        """Establishes a connection to queue"""
        try:
            conn = stomp.Connection(
                [(self.queue['host'], self.queue['port'])
                 ], vhost=self.queue['vhost'], heartbeats=(10000, 10000)
            )

            conn.connect(self.queue['username'],
                         self.queue['password'], wait=True)
            return conn
        except Exception as e:
            raise e

    def send_index_data(self, data):
        """Indexes data"""
        try:
            conn = self.connect_queue()
            conn.send(body=json.dumps(data), destination=self.queue.queue)
            conn.disconnect()
        except Exception as e:
            raise e
