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

import graphrepo.utils as utl
import graphrepo.models.relationships as rel
from graphrepo import models as mdl
from py2neo import NodeMatcher


class Commit(mdl.CustomNode):
    """Commit OGM  - Mapps Commit from PyDriller to py2neo
    """

    def __init__(self, commit, config):
        """Instantiates a commit. If a graph is given
        the node is created in the graph
        :param commit: pydriller Commit object
        :param config: a Config object
        """
        self.node_type = "Commit"
        self.node_index = "hash"
        self.config = config
        self.project_id = config.PROJECT_ID

        self.commit = commit
        self.indexed = False

        self.author_dates = {
            'author_datetime': self.commit.author_date.strftime(
                "%Y/%m/%d, %H:%M:%S"),
            'timestamp':  self.commit.author_date.timestamp(),
        }
        mdl.CustomNode.__init__(self, self.node_type,
                                hash=self.commit.hash,
                                project_id=self.project_id,
                                ** self.author_dates)

    def update_attributes(self, graph):
        """Updates custom attributes for commit node
        :param graph: py2neo graph object
        """
        self['is_merge'] = 1 if self.commit.merge else 0
        self['dmm_unit_size'] = self.commit.dmm_unit_size if self.commit.dmm_unit_size else -1
        self['dmm_unit_complexity'] = self.commit.dmm_unit_complexity if self.commit.dmm_unit_complexity else -1
        self['dmm_unit_interfacing'] = self.commit.dmm_unit_interfacing if self.commit.dmm_unit_interfacing else -1

        graph.push(self)

    def index_files_changed(self, graph, matcher):
        """Indexes the files changed by a commit
        :param graph: py2neo graph object
        """
        self.check_self(graph)
        for chg in self.commit.modifications:
            # Whenever a commit touches a method, the method
            # attributes are updated (e.g. loc or complexity)
            att = utl.get_file_attributes(chg)
            tpe = utl.get_file_change(chg)

            _file = matcher.match(
                "File", hash=utl.get_file_hash(chg),
                project_id=self.project_id).first()
            if not _file:
                _file = mdl.File(chg, self.project_id,
                                 graph=graph, file_type=True, **att)
            else:
                # update file atttributes
                utl.update_file_attributes(
                    att, tpe, _file, graph)
            # add update file relationship
            rel.UpdateFile(rel_from=self, rel_to=_file,
                           graph=graph, **self.author_dates,
                           **att,
                           **utl.get_file_metrics(chg))
            # index file methods and add relationship to change
            # methods in this commit
            self.index_methods_changed(chg, _file, graph, matcher)

    def index_methods_changed(self, change, file, graph, matcher):
        """Indexes all meethods changed in a commit and links methods to files
        :param change: pydriller Change object
        :param file: py2neo file object
        :param graph: py2neo Graph object
        :param matcher: py2neo NodeMatcher object
        """
        m_before = [m.name for m in change.methods_before]
        m_current = [m.name for m in change.methods]

        for met in change.changed_methods:
            metrics = utl.get_method_metrics(met)
            method = matcher.match("Method",
                                   hash=utl.get_method_hash(met, file),
                                   project_id=self.project_id).first()
            # create or update method
            if not method:
                method = mdl.Method(
                    met, file, self.project_id, graph=graph, **metrics)
                rel.HasMethod(rel_from=file, rel_to=method, graph=graph)
            else:
                utl.update_method_attributes(metrics, method, graph)
            # link method to commit
            m_type = utl.get_method_type(met, m_before, m_current)
            rel.UpdateMethod(rel_from=self, rel_to=method, type=m_type,
                             graph=graph, **metrics)
            # add delete relationship
            if m_type == 'DELETE':
                has_rel = graph.match_one([file, method], rel.HasMethod)
                if has_rel is not None:
                    graph.separate(has_rel)
                rel.HadMethod(rel_from=file, rel_to=method, graph=graph)

    def index_author(self, graph, matcher):
        """Indexes the commit author node in the graph
        and adds relationship to this commit
        :params graph: py2neo graph object
        :params matcher: py2neo NodeMatcher
        """
        self.check_self(graph)
        dev = matcher.match("Developer", name=self.commit.author.name,
                            email=self.commit.author.email).first()
        if not dev:
            dev = mdl.Developer(self.commit.author, graph=graph)
        rel.Authorship(rel_from=dev, rel_to=self, graph=graph)

    def index_parents(self, graph, repo, matcher):
        """This method chooses between indexing a parent
        relation or indexing a branch relationship between
        parent commits.
        :param graph: py2neo graph
        :param repo: pydrilller RepositoryManager
        :param matcher: py2neo NodeMatcher
        """
        if self.config.BRANCH_AS_NODE is True:
            self.index_parent(graph, matcher)
        else:
            self.index_parent_branch(graph, repo)

    def index_parent(self, graph, matcher):
        """For each parent of the commit, this method requests
        a commit object from pydriller's RepositoryMining object
        and indexes some data. If index_all_data is used, this method
        is applied recursively to all parents, however, this is
        very slow.
        :param graph: py2neo graph object
        :param matcher: py2neo NodeMatcher
        """
        self.check_self(graph)
        for parent in self.commit.parents:
            commit = matcher.match("Commit", hash=parent).first()
            if commit:
                rel.Parent(rel_from=commit, rel_to=self, graph=graph)

    def index_branch(self, graph, matcher):
        """Indexes branches
        :param graph: py2neo Graph object
        """
        branches = self.commit.branches
        for branch in branches:
            brn = matcher.match(
                "Branch", project_id=self.project_id, name=branch).first()
            if not brn:
                brn = mdl.Branch(
                    name=branch, project_id=self.project_id, graph=graph)
            rel.BelongsToBranch(rel_from=self, rel_to=brn,
                                graph=graph, name=branch)

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
            commit = mdl.Commit(repo.get_commit(parent), self.config)
            commit.index_author(graph)
            commit.index_date(graph)
            common_branches = self._common_branch(commit)
            for branch in common_branches:
                rel.BelongsToBranch(rel_from=commit, rel_to=self,
                                    graph=graph, name=branch)

    def index_date(self, graph, matcher):
        """Splits the date in year, month and day and creates
        the graph nodes and relationships
        :param graph: py2neo graph object
        """
        self.check_self(graph)

        date = self.commit.author_date
        day = matcher.match("Day", project_id=self.project_id,
                            hash=utl.get_day_hash(date)).first()
        if not day:
            day = mdl.Day(date, self.project_id,  graph=graph)

        month = matcher.match(
            "Month", project_id=self.project_id, hash=utl.get_month_hash(date)).first()
        if not month:
            month = mdl.Month(date, self.project_id, graph=graph)

        year = matcher.match(
            "Year", project_id=self.project_id, name=date.year).first()
        if not year:
            year = mdl.Year(date, self.project_id, graph=graph)

        rel.YearMonth(rel_from=year, rel_to=month, graph=graph)
        rel.YearMonth(rel_from=year, rel_to=month, graph=graph)
        rel.MonthDay(rel_from=month, rel_to=day, graph=graph)
        rel.DayCommit(rel_from=day, rel_to=self, graph=graph)

    def index_all_data(self, graph, matcher, repo=None):
        """Indexes all the data for a commit
        :param graph: py2neo graph object
        :param repo: PyDriller RepositoryMining class for the
          current repo
        """
        self.update_attributes(graph=graph)
        self.check_self(graph)
        self.index_author(graph, matcher)
        self.index_files_changed(graph, matcher)
        self.index_parents(graph, repo, matcher)
        self.index_branch(graph, matcher)

    def _common_branch(self, ot_commit):
        """Searches for a common branch between one commit
        and self
        :param ot_commit: another commit
        """
        oth_branches = ot_commit.commit.branches
        curr_branches = self.commit.branches
        return list((oth_branches).intersection(curr_branches))
