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

"""This module holds all possible relationships in the graph"""
from py2neo.data import Relationship


class CustomRelationship(Relationship):
    """Extends py2neo relationship object
    with custom functionality.
    """

    def __init__(self, rel_from=None, rel_to=None, graph=None, *args, **kwargs):
        """Instantiates a custom relationship. If a graph is given
        the relationship is indexed in the graph.
        :param rel_from: py2neo Node object
        :param rel_to: py2neo Node object
        :param graph: py2neo graph object
        """
        super().__init__(rel_from, rel_to, *args, **kwargs)
        if graph is not None:
            self.create(graph)

    def create(self, graph):
        graph.create(self)


class BelongsToBranch(CustomRelationship):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Authorship(CustomRelationship):
    pass


class Parent(CustomRelationship):
    pass


class YearMonth(CustomRelationship):
    pass


class MonthDay(CustomRelationship):
    pass


class DayCommit(CustomRelationship):
    pass


class UpdateFile(CustomRelationship):
    def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
        """Instantiates an Update relationship and creates a Neo4j relationship
        which also contains some module metrics extracted from Pydriller through
        Lizard.
        :param rel_from: Commit object
        :param rel_to: File object
        :param graph: Py2neo Graph object
        """
        super().__init__(rel_from, rel_to, graph,
                         *args, **kwargs)


class HasMethod(CustomRelationship):
    def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
        """Instantiates a Method relationship and creates a Neo4j relationship
        :param rel_from: Update object
        :param rel_to: Method Node
        :param graph: Py2neo Graph
        """
        super().__init__(rel_from, rel_to, graph, *args, **kwargs)


class HadMethod(CustomRelationship):
    def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
        """Instantiates a HadMethod relationship and creates a Neo4j relationship
        :param rel_from: Update object
        :param rel_to: Method Node
        :param graph: Py2neo Graph
        """
        super().__init__(rel_from, rel_to, graph, *args, **kwargs)


class UpdateMethod(CustomRelationship):
    def __init__(self, rel_from, rel_to, graph, type='ADD', *args, **kwargs):
        """Instantiates an UpdateMethod relationship and creates a Neo4j relationship
        :param rel_from: Update object
        :param rel_to: Method Node
        :param graph: Py2neo Graph
        """
        super().__init__(rel_from, rel_to, graph, type=type,
                         *args, **kwargs)


class FileType(CustomRelationship):
    pass
