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


class Update(CustomRelationship):
  def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
    """Instantiates an Update relationship and creates a Neo4j relationship
    which also contains some module metrics extracted from Pydriller through
    Lizard.
    :param rel_from: Commit object
    :param rel_to: File object
    :param graph: Py2neo Graph object
    """
    metrics = self.get_metrics(rel_to)
    super().__init__(rel_from, rel_to, graph, *args, **kwargs, **metrics)

  def get_metrics(self, change):
    """Creates and returns a dic with different metrics for a file
    :param commit: Commit object
    :returns: dic
    """
    return {
        'added': change.file.added,
        'removed': change.file.removed,
        'complexity': change.file.complexity,
        'nloc': change.file.nloc,
        'type': change.file.change_type.name,
        'token_count': change.file.token_count,
    }


class HasMethod(CustomRelationship):
  def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
    """Instantiates a Method relationship and creates a Neo4j relationship
    :param rel_from: Update object
    :param rel_to: Method Node
    :param graph: Py2neo Graph
    """
    super().__init__(rel_from, rel_to, graph, *args, **kwargs)


class UpdatedMethod(CustomRelationship):
  def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
    """Instantiates an UpdateMethod relationship and creates a Neo4j relationship
    :param rel_from: Update object
    :param rel_to: Method Node
    :param graph: Py2neo Graph
    """
    pass


class AddedMethod(CustomRelationship):
  def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
    """Instantiates an AddMethod relationship and creates a Neo4j relationship
    :param rel_from: Update object
    :param rel_to: Method Node
    :param graph: Py2neo Graph
    """
    pass


class RenamedMethod(CustomRelationship):
  def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
    """Instantiates a RenameMethod relationship and creates a Neo4j relationship
    :param rel_from: Update object
    :param rel_to: Method Node
    :param graph: Py2neo Graph
    """
    pass


def RemovedMethod(CustomRelationship):
  def __init__(self, rel_from, rel_to, graph, *args, **kwargs):
    """Instantiates a RemoveMethod relationship and creates a Neo4j relationship
    :param rel_from: Update object
    :param rel_to: Method Node
    :param graph: Py2neo Graph
    """
    pass


class Filetype(CustomRelationship):
  pass
