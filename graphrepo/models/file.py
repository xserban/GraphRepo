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
import graphrepo.utils as utl
import graphrepo.models.relationships as rel
from graphrepo.models.custom_node import CustomNode
from graphrepo.models.method import Method


class File(CustomNode):
    """File OGM Node - Maps files changed in a commit
    to py2neo objects
    """

    def __init__(self, file, project_id=None, graph=None,
                 file_type=True, *args, **kwargs):
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

        _hash = utl.get_file_hash(self.file)
        super().__init__(self.node_type, hash=_hash,
                         name=file.filename,
                         project_id=project_id,
                         type=utl.get_file_change(file),
                         *args, **kwargs)

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
        _hash = utl.get_file_type_hash(_name)
        super().__init__(self.node_type, hash=_hash, name=_name,
                         project_id=project_id)

        if graph is not None:
            self.index(graph)
