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
from graphrepo.drillers.driller import Driller
from graphrepo.drillers.cache_driller import CacheDriller


class TestCommit:
    """Most data is indexed when indexing a commmit
    so this class tests indexing for multiple models"""

    def test_nodes_index(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        # test that all nodes were indexed
        node_matcher = NodeMatcher(test_driller.graph)
        all_commits = list(node_matcher.match("Commit"))
        assert len(all_commits) == 8

        all_devs = list(node_matcher.match("Developer"))
        assert len(all_devs) == 2

        all_files = list(node_matcher.match("File"))
        assert len(all_files) == 6

        all_methods = list(node_matcher.match("Method"))
        assert len(all_methods) == 5

        all_branches = list(node_matcher.match("Branch"))
        assert len(all_branches) == 1

        test_driller.clean()

    def test_rel_index(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        # test that all relationships were indexed
        rel_matcher = RelationshipMatcher(test_driller.graph)

        all_branch = list(rel_matcher.match(None, "BranchCommit"))
        assert len(all_branch) == 8

        all_authorship = list(rel_matcher.match(None, "Author"))
        assert len(all_authorship) == 8

        all_parent = list(rel_matcher.match(None, "Parent"))
        assert len(all_parent) == 8

        all_updadedfile = list(rel_matcher.match(None, "UpdateFile"))
        assert len(all_updadedfile) == 9

        all_hasmethod = list(rel_matcher.match(None, "Method"))
        assert len(all_hasmethod) == 5

        all_updatemethod = list(rel_matcher.match(None, "UpdateMethod"))
        assert len(all_updatemethod) == 9

        test_driller.clean()

    def test_rel_index_cache(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = CacheDriller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch_cache_sequential()

        # test that all relationships were indexed
        rel_matcher = RelationshipMatcher(test_driller.graph)

        all_branch = list(rel_matcher.match(None, "BranchCommit"))
        assert len(all_branch) == 8

        all_authorship = list(rel_matcher.match(None, "Author"))
        assert len(all_authorship) == 8

        all_parent = list(rel_matcher.match(None, "Parent"))
        assert len(all_parent) == 8

        all_updadedfile = list(rel_matcher.match(None, "UpdateFile"))
        assert len(all_updadedfile) == 9

        all_hasmethod = list(rel_matcher.match(None, "Method"))
        assert len(all_hasmethod) == 5

        all_updatemethod = list(rel_matcher.match(None, "UpdateMethod"))
        assert len(all_updatemethod) == 9

        test_driller.clean()

    def test_custom_attributes_rel(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = Driller(os.path.join(folder, 'cnfg_simple.yml'))
        test_driller.drill_batch()

        node_matcher = NodeMatcher(test_driller.graph)
        rel_matcher = RelationshipMatcher(test_driller.graph)

        commit = node_matcher.match(
            "Commit", hash="aa6fa504ccb0fa919acc3cb31e510dc2048314eb0656f34babada15c").first()
        assert commit['is_merge'] == 0

        update_file_rel = rel_matcher.match([commit], "UpdateFile").first()
        assert update_file_rel['complexity'] == 2
        assert update_file_rel['nloc'] == 8
        assert update_file_rel['old_path'] == 'gr_test/default_class.py'
        assert update_file_rel['path'] == 'gr_test/default_class.py'
        assert update_file_rel['token_count'] == 42
        assert update_file_rel['type'] == 'MODIFY'
        assert update_file_rel['removed'] == 6
        assert update_file_rel['added'] == 0

        update_method_rel = rel_matcher.match(
            [commit], 'UpdateMethod').first()
        # assert update_method_rel['type'] == 'DELETE'
        assert update_method_rel['nloc'] == 5
        assert update_method_rel['complexity'] == 2
        assert update_method_rel['token_count'] == 21
        assert update_method_rel['length'] == 5
        assert update_method_rel['fan_in'] == 0
        assert update_method_rel['fan_out'] == 0
        assert update_method_rel['start_line'] == 11
        assert update_method_rel['end_line'] == 15

        test_driller.clean()
