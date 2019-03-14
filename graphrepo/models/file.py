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


class File(CustomNode):
  """File OGM Node - Maps files changed in a commit
  to py2neo objects
  """

  def __init__(self, file, graph=None, file_type=True):
    """Instantiates file object. If a graph is provided
    the node is also added to neo4j
    :param file: pydriller Modification object
    :param graph: py2neo graph object
    :param file_type: flag which decides if the file type
      should be indexed
    """
    self.node_type = "File"
    self.node_index = "hash"

    self.file = file
    _hash = hashlib.sha224(str(file.filename).encode('utf-8')).hexdigest()
    super().__init__(self.node_type, hash=_hash, name=file.filename)

    if graph is not None:
      self.index(graph)

    if file_type is True:
      self.index_type(graph=graph)

  def index_type(self, graph):
    """Creates file type if it does not exist and adds filetype
    relationship
    :param graph: py2neo Graph object
    """
    self.file_type = Filetype(self.file, graph=graph)
    rel.Filetype(self.file_type, self, graph=graph)


class Filetype(CustomNode):
  """Filetype OGM Node - Maps file types to py2neo object
  """

  def __init__(self, file, graph=None):
    """Instantiate Filetype object. If a graph is provided
    the node is also added to neo4j
    :param file: pydriller Modification object
    :param graph: py2neo graph object
    """
    self.node_type = "Filetype"
    self.node_index = "hash"

    _name = '.' + file.filename.split('.')[-1:][0]
    _hash = hashlib.sha224(_name.encode('utf-8')).hexdigest()
    super().__init__(self.node_type, hash=_hash, name=_name)
    if graph is not None:
      self.index(graph)
