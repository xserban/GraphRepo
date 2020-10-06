import graphrepo.drillers.batch_utils as utils


def create_hash_constraints(graph):
    """Creates uniqueness constratins on nodes' hash"""
    query = """CREATE CONSTRAINT ON (n: {}) ASSERT n.hash IS UNIQUE"""
    nodes = ["Developer", "Branch", "Commit", "File", "Method"]
    for n in nodes:
        q = query.format(n)
        graph.run(q)


def create_indices(graph):
    """Initializes all indexes for database"""
    utils.create_index_authors(graph)
    utils.create_index_branches(graph)
    utils.create_index_commits(graph)
    utils.create_index_files(graph)
    utils.create_index_methods(graph)
