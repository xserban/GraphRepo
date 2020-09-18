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
import json
import pika

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


class RabbitDriller(QueueDriller):
    """RabbitDriller class - parses a git repo and publishes
    the data in a queue every n commits
    """

    def connect_queue(self):
        """Establishes a connection to queue"""
        try:
            credentials = pika.PlainCredentials(
                self.queue['username'], self.queue['password'])
            self.con_parameters = pika.ConnectionParameters(self.queue['host'],
                                                            self.queue['port'],
                                                            self.queue['vhost'],
                                                            credentials)
            connection = pika.BlockingConnection(
                self.con_parameters)
            channel = connection.channel()

            channel.queue_declare(queue=self.queue['queue'], durable=True)
            return connection, channel
        except Exception as e:
            raise e

    def send_index_data(self, data):
        """Indexes data"""
        try:
            connection, channel = self.connect_queue()
            channel.basic_publish(
                exchange='',
                routing_key=self.queue['queue'],
                body=json.dumps(data),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))
            connection.close()
        except Exception as e:
            raise e
