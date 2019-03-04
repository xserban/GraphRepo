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

"""This module is a mapping between Pydriller Commit and neo4j """
import graphrepo.models.relationships as rel

from graphrepo.models.custom_node import CustomNode
from graphrepo.models.developer import Developer
from graphrepo.models.file import File
from graphrepo.models.day import Day
from graphrepo.models.month import Month
from graphrepo.models.year import Year

class Commit(CustomNode):
  """Commit OGM  - Mapps Commit from PyDriller to py2neo
  """
  def __init__(self, commit, graph=None, repo=None):
    """Instantiates a commit. If a graph is given
    the node is created in the graph
    :param commit: pydriller Commit object
    :param graph: py2neo Graph object
    :param repo: pydriller RepositoryMining object
    """
    self.node_type="Commit"
    self.node_index = "hash"

    self.commit = commit
    self.indexed = False
    CustomNode.__init__(self, self.node_type, hash=self.commit.hash)

    if graph is not None:
      self.index_all_data(graph=graph, repo=repo)

  def index_files_changed(self, graph):
    """Indexes the files changed by a commit
    :param graph: py2neo graph object
    """
    self.check_self(graph)
    for chg in self.commit.modifications:
      change = File(chg, graph=graph)
      rel.File(rel_from=self, rel_to=change, graph=graph)

  def index_author(self, graph):
    """Indexes the commit author node in the graph
    and adds relationship to this commit
    :params graph: py2neo graph object
    """
    self.check_self(graph)
    dev = Developer(self.commit.author, graph=graph)
    rel.Authorship(dev, self, graph=graph)

  def index_parents(self, graph, repo):
    """For each parent of the commit, this method requests
    a commit object from pydriller's RepositoryMining object
    and indexes some data. If index_all_data is used, this method
    is applied recursively to all parents, however, this is
    very slow.
    :param graph: py2neo graph object
    :param repo: PyDriller RepositoryMining class for the
      current repo
    """
    self.check_self(graph)
    for parent in self.commit.parents:
      commit = Commit(repo.get_commit(parent))
      commit.index_author(graph)
      commit.index_date(graph)
      # commit.index_all_data(graph, repo)
      rel.Parent(commit, self, graph=graph)

  def index_date(self, graph):
    """Splits the date in year, month and day and creates
    the graph nodes and relationships
    :param graph: py2neo graph object
    """
    self.check_self(graph)

    date = self.commit.author_date
    day = Day(date, graph=graph)
    month = Month(date, graph=graph)
    year = Year(date, graph=graph)

    rel.YearMonth(year, month, graph=graph)
    rel.YearMonth(year, month, graph=graph)
    rel.MonthDay(month, day, graph=graph)
    rel.DayCommit(day, self, graph=graph)


  def index_all_data(self, graph, repo=None):
    """Indexes all the data for a commit
    :param graph: py2neo graph object
    :param repo: PyDriller RepositoryMining class for the
      current repo
    """
    self.check_self(graph)
    self.index_author(graph)
    self.index_date(graph)
    self.index_files_changed(graph)

    if repo is not None:
      self.index_parents(graph, repo)
