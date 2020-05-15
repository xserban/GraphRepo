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

"""This module is a mapping to a neo4j node for a file and filetype"""
import hashlib

import graphrepo.models.relationships as rel
from graphrepo.models.custom_node import CustomNode
from graphrepo.models.method import Method


class File(CustomNode):
    """File OGM Node - Maps files changed in a commit
    to py2neo objects
    """

    def __init__(self, file, project_id=None, graph=None, file_type=True):
        """Instantiates file object. If a graph is provided
        the node is also added to neo4j
        :param file: pydriller Modification object
        :param project_id: a string identifying the project a file belogns to
        :param graph: py2neo graph object
        :param file_type: flag which decides if the file type
          should be indexed
        """
        self.node_type = "File"
        self.node_index = "hash"
        self.project_id = project_id

        self.file = file
        att = self.get_update_attributes()
        _hash = hashlib.sha224(str(file.filename).encode('utf-8')).hexdigest()
        super().__init__(self.node_type, hash=_hash,
                         name=file.filename,
                         project_id=project_id,
                         **att)

        if graph is not None:
            self.index(graph)

        if file_type is True:
            self.index_type(graph=graph)

    def index_type(self, graph):
        """Creates file type if it does not exist and adds filetype
        relationship
        :param graph: py2neo Graph object
        """
        self.file_type = FileType(self.file, self.project_id, graph=graph)
        rel.FileType(self.file_type, self, graph=graph)

    def get_update_attributes(self):
        """Updates file attributes
        :returns: dictionary with custom node attributes
        """
        return {
            'old_path': self.file.old_path if self.file.old_path else '',
            'new_path': self.file.new_path if self.file.new_path else '',
            'source_code': self.file.source_code if self.file.source_code else '',
            'source_code_before':  self.file.source_code_before if self.file.source_code_before else '',
            'nloc': self.file.nloc if self.file.nloc else -1,
            'complexity': self.file.complexity if self.file.complexity else -1,
            'token_count': self.file.token_count if self.file.token_count else -1,
        }

    def index_methods(self, graph, commit=None, *args, **kwargs):
        """Indexes latest methods and adds a relation
        between commit and the methods changed in the commit
        if the commit object is given
        :param graph: py2neo Graph object
        :param commit: GraphRepo Commit object
        """
        # index new or changed methods
        for met in self.file.methods:
            method = Method(met, self.project_id, graph=graph)
            rel.HasMethod(rel_from=self, rel_to=method, graph=graph)
            if met in self.file.changed_methods:
                type_ = self._get_method_type(met)
                rel.UpdateMethod(rel_from=commit, rel_to=method,
                                 type=type_, graph=graph,
                                 *args, **kwargs)

        if len(self.file.methods):
            self.update_deleted_methods(graph, commit, *args, **kwargs)

    def update_deleted_methods(self, graph, commit, *args, **kwargs):
        """Indexes latest methods and adds a relation
        between commit and the methods changed in the commit
        if the commit object is given
        :param graph: py2neo Graph object
        :param commit: GraphRepo Commit object
        """
        for met in self.file.methods_before:
            if met not in self.file.methods:
                method = Method(met, self.project_id, graph=graph)
                # add relationship from commit to method
                rel.UpdateMethod(rel_from=commit, rel_to=method,
                                 type='DELETE', graph=graph, *args, **kwargs)
                # replace relationship from file to method from HasMethod to HadMethod
                has_rel = graph.match_one([self, method], rel.HasMethod)
                # TODO: Test this better
                if has_rel:
                    graph.separate(has_rel)
                rel.HadMethod(rel_from=self, rel_to=method, graph=graph)

    def _get_method_type(self, met):
        """Checks if the method existed before and it is updated"""
        type_ = "ADD"
        for m in self.file.methods_before:
            if m.name == met.name:
                return "MODIFY"
        return type_


class FileType(CustomNode):
    """Filetype OGM Node - Maps file types to py2neo object
    """

    def __init__(self, file, project_id=None, graph=None):
        """Instantiate Filetype object. If a graph is provided
        the node is also added to neo4j
        :param file: pydriller Modification object
        :param project_id: a string identifying the project a file belogns to
        :param graph: py2neo graph object
        """
        self.node_type = "FileType"
        self.node_index = "hash"

        _name = '.' + file.filename.split('.')[-1:][0]
        _hash = hashlib.sha224(_name.encode('utf-8')).hexdigest()
        super().__init__(self.node_type, hash=_hash, name=_name,
                         project_id=project_id)
        if graph is not None:
            self.index(graph)
