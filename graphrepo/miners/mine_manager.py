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
from py2neo import Graph, NodeMatcher, RelationshipMatcher
from graphrepo.config import Config
from graphrepo.logger import Logger
from graphrepo.singleton import Singleton
from graphrepo import miners
from graphrepo.miners import mappers


LG = Logger()


class MineManager(metaclass=Singleton):
    """MineManageer class - This class manages custom
    miners. At the moment we instantiate all miners,
    but other managers which handle different 'teams of miners'
    can be created.
    """

    def __init__(self):
        """Initializes the properties of this class"""
        self.config = Config()
        self.graph = None
        self.node_matcher = None
        self.rel_matcher = None

    def configure(self, db_url="localhost",
                  port=13000, db_user="neo4j",
                  db_pwd="neo4j"):
        """Sets the application constants"""
        # TODO: validate inputs
        self.config.DB_URL = db_url
        self.config.PORT = port
        self.config.DB_USER = db_user
        self.config.DB_PWD = db_pwd
        self.connect()

    def connect(self):
        """Instantiates the connection to Neo4j and stores
        the graph internally.
        Throws exception if the connection can not pe realized
        """
        try:
            self.graph = Graph(host=self.config.DB_URL,
                               user=self.config.DB_USER,
                               password=self.config.DB_PWD,
                               http_port=self.config.PORT)
            self.node_matcher = NodeMatcher(self.graph)
            self.rel_matcher = RelationshipMatcher(self.graph)
            self.init_miners()
        except Exception as exc:
            LG.log_and_raise(exc)

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

    def init_miners(self):
        """Initializes all miners"""
        try:
            # TODO: Parse this automatically?
            self.commit_miner = miners.CommitMiner(
                graph=self.graph,
                node_matcher=self.node_matcher,
                rel_matcher=self.rel_matcher)
            self.dev_miner = miners.DeveloperMiner(graph=self.graph,
                                                   node_matcher=self.node_matcher,
                                                   rel_matcher=self.rel_matcher)
            self.file_miner = miners.FileMiner(graph=self.graph,
                                               node_matcher=self.node_matcher,
                                               rel_matcher=self.rel_matcher)
            self.method_miner = miners.MethodMiner(graph=self.graph,
                                                   node_matcher=self.node_matcher,
                                                   rel_matcher=self.rel_matcher)

        except Exception as exc:
            LG.log_and_raise(exc)
        else:
            return

    def get_all_data(self, map=False, merge=False):
        """Returns all nodes and relationships from Neo4j
        :param map: Map data using default mappers for nodes and rels
        :param merge: Concatenates nodes an relationships
        :returns: if merge is False it returns a tuple with two
          arrays: the first with nodes, the second with relationships
          if merge is True it returns only one array
        """
        nodes = self.node_matcher.match()
        rels = self.rel_matcher.match()

        if map is True:
            nodes = [mappers.node.NodeMapper.map_default_node(
                n) for n in nodes]
            rels = [mappers.rels.RelMapper.map_default_rel(r) for r in rels]
            if merge is True:
                return nodes+rels, None

        return nodes, rels
