import os

from graphrepo.drillers.default import DefaultDriller
import graphrepo.drillers.db_init as db_init

from py2neo.database import Schema


class TestDBInit:
    def test_hash_constraints(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = DefaultDriller(os.path.join(folder, 'cnfg_simple.yml'))

        db_init.create_hash_constraints(test_driller.graph)

        schm = Schema(test_driller.graph)

        labels = ["Developer", "Branch", "Commit", "File", "Method"]

        for l in labels:
            c = schm.get_uniqueness_constraints(l)
            assert len(c) == 1

        # clean
        for l in labels:
            schm.drop_uniqueness_constraint(l, 'hash')

    def test_indices(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        test_driller = DefaultDriller(os.path.join(folder, 'cnfg_simple.yml'))

        db_init.create_indices(test_driller.graph)

        schm = Schema(test_driller.graph)

        index_authors = schm.get_indexes("Developer")
        assert len(index_authors) == 1

        index_branch = schm.get_indexes("Branch")
        assert len(index_branch) == 2

        index_commits = schm.get_indexes("Commit")
        assert len(index_commits) == 2

        index_files = schm.get_indexes("File")
        assert len(index_files) == 2

        index_methods = schm.get_indexes("Method")
        assert len(index_methods) == 2

        # clean
        schm.drop_index("Developer", "hash")
        schm.drop_index("Branch", "hash")
        schm.drop_index("Branch", "project_id")
        schm.drop_index("Commit", "hash")
        schm.drop_index("Commit", "project_id")
        schm.drop_index("File", "hash")
        schm.drop_index("File", "project_id")
        schm.drop_index("Method", "hash")
        schm.drop_index("Method", "project_id")
