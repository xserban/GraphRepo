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

from graphrepo import models as mdl
from graphrepo.config import Config

CT = Config()


class Commit(mdl.CustomNode):
  """Commit OGM  - Mapps Commit from PyDriller to py2neo
  """

  def __init__(self, commit, graph=None, repo=None):
    """Instantiates a commit. If a graph is given
    the node is created in the graph
    :param commit: pydriller Commit object
    :param graph: py2neo Graph object
    :param repo: pydriller RepositoryMining object
    """
    self.node_type = "Commit"
    self.node_index = "hash"

    self.commit = commit
    self.indexed = False
    mdl.CustomNode.__init__(self, self.node_type, hash=self.commit.hash)

    if graph is not None:
      self.index_all_data(graph=graph, repo=repo)

  def index_files_changed(self, graph):
    """Indexes the files changed by a commit
    :param graph: py2neo graph object
    """
    self.check_self(graph)
    for chg in self.commit.modifications:
      change = mdl.File(chg, graph=graph)
      rel.Update(rel_from=self, rel_to=change, graph=graph)
      # Whenever a commit touches a method, the method
      # attributes are updated (e.g. loc or complexity)
      self.index_all_file_methods(graph, chg, change)

  def index_all_file_methods(self, graph, modification, file):
    """Indexes all methods from a commit file
    :param graph: py2neo graph object
    """
    for met in modification.methods:
      method = mdl.Method(met, graph=graph)
      rel.HasMethod(rel_from=file, rel_to=method, graph=graph)

  def index_changed_methods(self, graph):
    """Indexes all methods changed by a commig
    :param graph: py2neo graph object
    """
    self.check_self(graph)
    all_methods = []
    for chg in self.commit.modifications:
      # collect methods changed
      pass

  def parse_changed_methods(self, change):
    """Given a commit change, parses methods
    touched by the commit"""
    pass

  def index_author(self, graph):
    """Indexes the commit author node in the graph
    and adds relationship to this commit
    :params graph: py2neo graph object
    """
    self.check_self(graph)
    dev = mdl.Developer(self.commit.author, graph=graph)
    rel.Authorship(rel_from=dev, rel_to=self, graph=graph)

  def index_parents(self, graph, repo, branch=CT.BRANCH_AS_NODE):
    """This method chooses between indexing a parent
    relation or indexing a branch relationship between
    parent commits.
    :param graph: py2neo graph
    """
    if branch is True:
      self.index_parent(graph, repo)
    else:
      self.index_parent_branch(graph, repo)

  def index_parent(self, graph=None, repo=None):
    """For each parent of the commit, this method requests
    a commit object from pydriller's RepositoryMining object
    and indexes some data. If index_all_data is used, this method
    is applied recursively to all parents, however, this is
    very slow.
    :param graph: py2neo graph object
    :param repo: PyDriller RepositoryMining object
    """
    self.check_self(graph)
    for parent in self.commit.parents:
      commit = mdl.Commit(repo.get_commit(parent))
      commit.index_author(graph)
      commit.index_date(graph)
      # commit.index_all_data(graph, repo)
      rel.Parent(rel_from=commit, rel_to=self, graph=graph)
      # index branches
      branches = self.commit.branches
      for branch in branches:
        br = mdl.Branch(name=branch, graph=graph)
        rel.BelongsToBranch(rel_from=self, rel_to=br, graph=graph, name=branch)

  def index_parent_branch(self, graph, repo):
    """For each parent of the commit, this method requests
    a commit object from pydriller's RepositoryMining object
    and indexes a branch relationship between the two and
    the parent commit data
    :param graph: py2neo Graph object
    :param repo: Pydriller RepositoryMining object
    """
    self.check_self(graph)
    for parent in self.commit.parents:
      commit = mdl.Commit(repo.get_commit(parent))
      commit.index_author(graph)
      commit.index_date(graph)
      common_branches = self._common_branch(commit)
      for branch in common_branches:
        rel.BelongsToBranch(rel_from=commit, rel_to=self,
                            graph=graph, name=branch)

  def index_date(self, graph):
    """Splits the date in year, month and day and creates
    the graph nodes and relationships
    :param graph: py2neo graph object
    """
    self.check_self(graph)

    date = self.commit.author_date
    day = mdl.Day(date, graph=graph)
    month = mdl.Month(date, graph=graph)
    year = mdl.Year(date, graph=graph)

    rel.YearMonth(rel_from=year, rel_to=month, graph=graph)
    rel.YearMonth(rel_from=year, rel_to=month, graph=graph)
    rel.MonthDay(rel_from=month, rel_to=day, graph=graph)
    rel.DayCommit(rel_from=day, rel_to=self, graph=graph)

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

  def _common_branch(self, ot_commit):
    """Searches for a common branch between one commit
    and self
    :param ot_commit: another commint
    """
    oth_branches = ot_commit.commit.branches
    curr_branches = self.commit.branches
    return list((oth_branches).intersection(curr_branches))
