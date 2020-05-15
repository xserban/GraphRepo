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

from graphrepo.driller import Driller
from graphrepo.utils import parse_config
from graphrepo.miners.file import FileMiner
from py2neo import NodeMatcher, RelationshipMatcher


class TestFileMiner:
    def test_get_all(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        neo, project = parse_config(os.path.join(folder, 'cnfg_simple.yml'))

        test_driller = Driller()
        test_driller.configure(**neo, **project)
        test_driller.connect()
        test_driller.drill()

        n_matcher = NodeMatcher(test_driller.graph)
        r_matcher = RelationshipMatcher(test_driller.graph)

        f_miner = FileMiner(test_driller.graph, n_matcher, r_matcher)

        all_files = f_miner.get_all()
        assert len(all_files) == 5

        # get readme file
        readme = f_miner.query(name='README.MD')
        assert readme['name'] == 'README.MD'

        # get file history
        update_history = f_miner.get_change_history(
            {'hash': '82f8febc140d8a07927358e738e7bcb89e162b5612c5b2b769606fe2'})
        assert len(update_history) == 5

        test_driller.clean()
