# Copyright 2020 NullConvergence
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime
import os

from py2neo import NodeMatcher, RelationshipMatcher
from graphrepo.drillers.driller import Driller
from graphrepo.miners.commit import CommitMiner


class TestCommitMiner:
    def test_gets(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        st_date = datetime.strptime(
            '14 May, 2020 00:00', '%d %B, %Y %H:%M').timestamp()
        end_date = datetime.strptime(
            '15 May, 2020 02:00', '%d %B, %Y %H:%M').timestamp()

        n_matcher = NodeMatcher(test_driller.graph)
        r_matcher = RelationshipMatcher(test_driller.graph)

        com_miner = CommitMiner(test_driller.graph, n_matcher, r_matcher)

        all_com = com_miner.get_all()
        assert len(all_com) == 8

        all_com_dates = com_miner.get_between_dates(st_date, end_date)
        assert len(all_com_dates) == 8

        c_files = com_miner.get_commit_files(
            'ad98f8594c15b1ebc4be4f20d849bcc0edf69ec574c33dfd84b7792d')
        assert len(c_files) == 3

        c_file_updates = com_miner.get_commit_file_updates(
            'ad98f8594c15b1ebc4be4f20d849bcc0edf69ec574c33dfd84b7792d')
        assert len(c_file_updates) == 3

        c_methods = com_miner.get_commit_methods(
            'ad98f8594c15b1ebc4be4f20d849bcc0edf69ec574c33dfd84b7792d')
        assert len(c_methods) == 3

        c_method_updates = com_miner.get_commit_method_updates(
            'ad98f8594c15b1ebc4be4f20d849bcc0edf69ec574c33dfd84b7792d')
        assert len(c_method_updates) == 3

        test_driller.clean()
