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
"""This module is a custom miner class with some abstractions"""
from abc import abstractmethod


class DefaultMiner():
    """The miners are currently synchronous, but
    ideally they will be async in the future"""

    def __init__(self, graph, node_matcher, rel_matcher, *args, **kwargs):
        self.graph = graph
        self.node_matcher = node_matcher
        self.rel_matcher = rel_matcher

    @abstractmethod
    def get_all(self):
        """This method returns all artifacts
        found by a miner"""
        raise NotImplementedError
