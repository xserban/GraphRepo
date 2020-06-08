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

from graphrepo.drillers.cache_driller import CacheDriller


class TestCacheDriller:
    def test_indexing(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = CacheDriller(os.path.join(folder, 'cnfg_init.yml'))
        test_driller.drill_batch_cache_sequential()
        records = [r for r in test_driller.graph.run(
            "MATCH(n) RETURN n")]
        assert len(records) == 22

        test_driller.clean()

    def test_drill_batch_cache(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = CacheDriller(os.path.join(folder, 'cnfg_init.yml'))
        test_driller.drill_batch_cache_all()
        records = [r for r in test_driller.graph.run(
            "MATCH(n) RETURN n")]
        assert len(records) == 22

        test_driller.clean()
