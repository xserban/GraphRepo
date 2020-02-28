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

"""This module is a mapping to a neo4j node for a day"""
import hashlib

from graphrepo.models.custom_node import CustomNode


class Day(CustomNode):
  """Day node
  """

  def __init__(self, date, project_id=None, graph=None):
    """Instantiates a day object and hashes the month, year and
    day as an unique key for the day. We wish to simulate a time
    series (otherwise, each month could've connect to the same day).
    If a graph is provided, the object is indexed in neo4j
    :param date: datetime object containing all date info
    :param project_id: a string identifying the project a day belogns to
    """
    self.node_type = "Day"
    self.node_index = "hash"

    _hash = hashlib.sha224(
        (str(date.month) + str(date.year)
         + str(date.day)).encode('utf-8')).hexdigest()
    super().__init__(self.node_type, name=date.day, hash=_hash,
                     project_id=project_id)
    if graph is not None:
      self.index(graph)
