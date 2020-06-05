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

import os
import pytest
import yaml

from py2neo import NodeMatcher, RelationshipMatcher
from graphrepo.driller import Driller
from graphrepo.utils import parse_config
from graphrepo.miners.developer import DeveloperMiner


class TestDevMiner:
    def test_get_all(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        n_matcher = NodeMatcher(test_driller.graph)
        r_matcher = RelationshipMatcher(test_driller.graph)

        dev_miner = DeveloperMiner(test_driller.graph, n_matcher, r_matcher)

    def test_get_commits(self):
        pass

    def test_get_files(self):
        pass

    def test_get_files_updates(self):
        pass

    def test_get_methods(self):
        pass
