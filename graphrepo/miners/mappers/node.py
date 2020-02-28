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
"""This module is a custom node mapper, which translates
the neo4j node models to custom data structures, e.g. dictionaries """

from graphrepo.miners.mappers.default import DefaultMapper


class NodeMapper(DefaultMapper):
  """The miners are currently synchronous, but
  ideally they will be async in the future"""

  def __init__(self, *args, **kwargs):
    """Default Init"""
    super().__init__(*args, **kwargs)

  @classmethod
  def map_default_node(cls, node):
    """Maps a node to a dictionary"""
    return {
        'data': {
            'id': cls.get_id(node),
            'label': cls.get_label(node),
            'type': list(node._labels)[0],
            'name': node['name']
        }
    }

  @classmethod
  def get_id(cls, node):
    """Returns node default identifier"""
    return node.identity

  @classmethod
  def get_label(cls, node):
    """Returns node default label"""
    return node['name'] if node['name'] else node['hash']
