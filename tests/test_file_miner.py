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

from py2neo import NodeMatcher, RelationshipMatcher
from graphrepo.drillers.driller import Driller
from graphrepo.miners.file import FileMiner


class TestFileMiner:
    def test_get_all(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        n_matcher = NodeMatcher(test_driller.graph)
        r_matcher = RelationshipMatcher(test_driller.graph)

        f_miner = FileMiner(test_driller.graph, n_matcher, r_matcher)

        all_files = f_miner.get_all()
        assert len(all_files) == 6

        # get readme file
        readme = f_miner.query(name='README.MD')
        assert readme['name'] == 'README.MD'

        # get file history
        f_hash = 'f85f4af5b20ddd617f93da13c7789a65fb972e68a8d634d5f253abab'
        update_history = f_miner.get_change_history(f_hash)
        assert len(update_history) == 3

        # test file get methods
        current_m = f_miner.get_current_methods(f_hash)
        assert len(current_m) == 2

        test_driller.clean()
