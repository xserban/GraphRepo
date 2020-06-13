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
from graphrepo.miners.method import MethodMiner


class TestMethodMiner:
    def test_get_all(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        n_matcher = NodeMatcher(test_driller.graph)
        r_matcher = RelationshipMatcher(test_driller.graph)

        m_miner = MethodMiner(test_driller.graph, n_matcher, r_matcher)

        all_methods = m_miner.get_all()
        assert len(all_methods) == 5
        m_hash = '417e845b5d0702fcb26954809407f0919dfa229308e520de01e0cf6e'
        met = m_miner.query(hash=m_hash)
        assert met['name'] == 'get_name'

        history = m_miner.get_change_history(m_hash)
        assert len(history) == 2

        test_driller.clean()
