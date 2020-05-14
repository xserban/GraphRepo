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


class MineManager():
    """MineManageer class - This class manages custom
    miners. At the moment we instantiate all miners,
    but other managers which handle different 'teams of miners'
    can be created.
    """

    def __init__(self, graph):
        """Initializes the properties of this class"""
        self.graph = graph
        self.node_matcher = NodeMatcher(graph)
        self.rel_matcher = RelationshipMatcher(graph)
        self.init_miners()

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

    def remove_all_data(self, project_id):
        """Removes all elements from a graph given a project id
        :param project_id: the project ids for the nodes to be removed
        """
        pass
        # self.graph.run()
