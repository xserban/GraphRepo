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


class TestDriller:
    def test_configure(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        neo, project = parse_config(os.path.join(folder, 'cnfg_init.yml'))
        test_driller = Driller()
        test_driller.configure(**neo, **project)

        assert test_driller.config.DB_URL == 'localhost'
        assert test_driller.config.REPO == 'tests/gr-test'

        test_driller.connect()
        assert test_driller.graph is not None

    def test_indexing(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        neo, project = parse_config(os.path.join(folder, 'cnfg_init.yml'))
        test_driller = Driller()

        test_driller.configure(**neo, **project)
        test_driller.connect()

        test_driller.drill()
        records = [r for r in test_driller.graph.run(
            "MATCH(n) RETURN n")]
        assert len(records) == 25

        test_driller.clean()
