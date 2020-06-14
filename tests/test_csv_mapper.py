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
from graphrepo.drillers import Driller
from graphrepo.mappers import CSVMapper
from graphrepo.miners import CommitMiner


class TestCSVMapper:
    """Most data is indexed when indexing a commmit
    so this class tests indexing for multiple models"""

    def test_csv_mapper(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        n_matcher = NodeMatcher(test_driller.graph)
        r_matcher = RelationshipMatcher(test_driller.graph)

        com_miner = CommitMiner(test_driller.graph, n_matcher, r_matcher)
        mapper = CSVMapper()

        commits = com_miner.get_all()
        mapped_commits = mapper.map(commits)
        assert mapped_commits.shape == (8, 9)

        c_files = com_miner.get_commit_files(
            'ad98f8594c15b1ebc4be4f20d849bcc0edf69ec574c33dfd84b7792d')
        c_csv = mapper.map(c_files)
        assert c_csv.shape == (3, 4)

        test_driller.clean()
