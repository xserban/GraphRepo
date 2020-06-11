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

from datetime import datetime
import os

from py2neo import NodeMatcher, RelationshipMatcher
from graphrepo.drillers.driller import Driller
from graphrepo.miners.developer import DeveloperMiner


class TestDevMiner:
    def test_gets(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        st_date = datetime.strptime(
            "14 May, 2020 00:00", '%d %B, %Y %H:%M').timestamp()
        end_date = datetime.strptime(
            "15 May, 2020 02:00", '%d %B, %Y %H:%M').timestamp()

        n_matcher = NodeMatcher(test_driller.graph)
        r_matcher = RelationshipMatcher(test_driller.graph)

        dev_miner = DeveloperMiner(test_driller.graph, n_matcher, r_matcher)

        all_devs = dev_miner.get_all()
        assert len(all_devs) == 2

        all_commits = dev_miner.get_commits(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb")
        assert len(all_commits) == 7

        all_com_id = dev_miner.get_commits(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb",
            project_id=test_driller.config.ct.project_id
        )
        assert len(all_com_id) == 7

        all_com_id_dates = dev_miner.get_commits(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb",
            project_id=test_driller.config.ct.project_id,
            start_date=st_date,
            end_date=end_date
        )
        assert len(all_com_id_dates) == 7

        all_files = dev_miner.get_files(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb"
        )
        assert len(all_files) == 6

        all_files_id_dates = dev_miner.get_files(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb",
            project_id=test_driller.config.ct.project_id,
            start_date=st_date,
            end_date=end_date
        )
        assert len(all_files_id_dates) == 6

        files_updates = dev_miner.get_files_updates(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb"
        )
        assert len(files_updates) == 9

        files_updates_id_dates = dev_miner.get_files_updates(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb",
            project_id=test_driller.config.ct.project_id,
            start_date=st_date,
            end_date=end_date
        )
        assert len(files_updates_id_dates) == 9

        all_methods = dev_miner.get_methods(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb"
        )
        assert len(all_methods) == 5

        all_methods_id_dates = dev_miner.get_methods(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb",
            project_id=test_driller.config.ct.project_id,
            start_date=st_date,
            end_date=end_date
        )
        assert len(all_methods_id_dates) == 5

        method_updates = dev_miner.get_method_updates(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb"
        )
        assert len(method_updates) == 9

        method_updates_id_dates = dev_miner.get_method_updates(
            dev_hash="bb1a1830d2f4f4d13151827aa1072ed43bd8738a139da332e1ee3ddb",
            project_id=test_driller.config.ct.project_id,
            start_date=st_date,
            end_date=end_date
        )
        assert len(method_updates_id_dates) == 9

        test_driller.clean()
