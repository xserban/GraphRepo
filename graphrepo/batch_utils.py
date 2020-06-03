from datetime import datetime


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def index_commits(graph, commits, batch_size=100):
    query = """
    UNWIND {commits} AS c
    MERGE (:Commit { hash: c.hash, timestamp: c.timestamp, is_merge: c.is_merge, project_id: c.project_id})
    """
    if batch_size:
        for b in batch(commits, batch_size):
            graph.run(query, commits=b)
    else:
        graph.run(query, commits=commits)


def index_authors(graph, authors, batch_size=100):
    query = """
    UNWIND {authors} AS a
    MERGE (:Author { hash: a.hash})
    """
    if batch_size:
        for b in batch(authors, batch_size):
            graph.run(query, authors=b)
    else:
        graph.run(query, authors=authors)


def index_branches(graph, branches, batch_size=100):
    query = """
    UNWIND {branches} AS a
    MERGE (:Branch { hash: a.hash, name:a.name, project_id: a.project_id})
    """
    for b in batch(branches, batch_size):
        graph.run(query, branches=b)


def index_branch_commits(graph, bc, batch_size=100):
    query = """
    UNWIND {ac} AS a
    MATCH (x:Branch),(y:Commit)
    WHERE x.hash = a.branch_hash AND y.hash = a.commit_hash
    MERGE (x)-[r:Branch{}]->(y)
    """
    for b in batch(bc, batch_size):
        graph.run(query, ac=b)


def index_files(graph, files, batch_size=100):
    query = """
    UNWIND {files} AS f
    MERGE (:File { hash: f.hash, project_id: f.project_id, type:f.type, name: f.name})
    """
    if batch_size:
        for b in batch(files, batch_size):
            graph.run(query, files=b)
    else:
        graph.run(query, files=files)


def index_methods(graph, methods, batch_size=100):
    query = """
    UNWIND {methods} AS f
    MERGE (:Method { hash: f.hash, project_id: f.project_id})
    """
    if batch_size:
        for b in batch(methods, batch_size):
            graph.run(query, methods=b)
    else:
        graph.run(query, methods=methods)


def index_author_commits(graph, ac, batch_size=100):
    query = """
    UNWIND {ac} AS a
    MATCH (x:Author),(y:Commit)
    WHERE x.hash = a.author_hash AND y.hash = a.commit_hash
    MERGE (x)-[r:Authorship{timestamp: a.timestamp}]->(y)
    """
    for b in batch(ac, batch_size):
        graph.run(query, ac=b)


def index_commit_files(graph, cf, batch_size=100):
    query = """
    UNWIND {cf} AS a
    MATCH (x:Commit),(y:File)
    WHERE x.hash = a.commit_hash AND y.hash = a.file_hash
    MERGE (x)-[r:UpdateFile{
                timestamp: a['attributes']['timestamp'],
                old_path: a['attributes']['old_path'],
                path: a['attributes']['path'],
                source_code: a['attributes']['source_code'],
                source_code_before: a['attributes']['source_code_before'],
                nloc: a['attributes']['nloc'],
                complexity: a['attributes']['complexity'],
                token_count: a['attributes']['token_count'],
                added: a['attributes']['added'],
                removed: a['attributes']['removed'],
                type: a['attributes']['type']
    }]->(y)
    """
    if batch_size:
        for b in batch(cf, batch_size):
            graph.run(query, cf=b)
    else:
        graph.run(query, cf=cf)


def index_file_methods(graph, cf, batch_size=100):
    query = """
    UNWIND {cf} AS a
    MATCH (x:File),(y:Method)
    WHERE x.hash = a.file_hash AND y.hash = a.method_hash
    MERGE (x)-[r:Method{}]->(y)
    """
    for b in batch(cf, batch_size):
        graph.run(query, cf=b)


def index_commit_method(graph, cm, batch_size=100):
    query = """
    UNWIND {cf} AS a
    MATCH (x:Commit),(y:Method)
    WHERE x.hash = a.commit_hash AND y.hash = a.method_hash
    MERGE (x)-[r:UpdateMethod{
                    timestamp: a['attributes']['timestamp'],
                    long_name: a['attributes']['long_name'],
                    parameters: a['attributes']['parameters'],
                    complexity: a['attributes']['complexity'],
                    nloc: a['attributes']['nloc'],
                    fan_in: a['attributes']['fan_in'],
                    fan_out: a['attributes']['fan_out'],
                    general_fan_out: a['attributes']['general_fan_out'],
                    length: a['attributes']['length'],
                    token_count: a['attributes']['token_count'],
                    start_line: a['attributes']['start_line'],
                    end_line: a['attributes']['end_line']
    }]->(y)
    """
    if batch_size:
        for b in batch(cm, batch_size):
            graph.run(query, cf=b)
    else:
        graph.run(query, cf=cm)


def create_index_authors(graph):
    query = """
    CREATE INDEX ON :Author(hash)
    """
    graph.run(query)


def create_index_commits(graph):
    query = """
    CREATE INDEX ON :Commit(hash)
    """
    graph.run(query)


def create_index_branches(graph):
    query = """
    CREATE INDEX ON :Branch(hash)
    """
    graph.run(query)


def create_index_files(graph):
    query = """
    CREATE INDEX ON :File(hash)
    """
    graph.run(query)


def create_index_methods(graph):
    query = """
    CREATE INDEX ON :Method(hash)
    """
    graph.run(query)


def index_all(graph, developers, commits, dev_commits, branches,
              branches_commits, files, commit_files, methods, file_methods,
              commit_methods, batch_size=100):

    developers = list({v['hash']: v for v in developers}.values())
    branches = list({v['hash']: v for v in branches}.values())
    branches_commits = list({str(i): i for i in branches_commits}.values())

    files = list({v['hash']: v for v in files}.values())
    methods = list({v['hash']: v for v in methods}.values())
    file_methods = list({str(i): i for i in file_methods}.values())
    total = datetime.now()

    print('Indexing ', len(developers), ' authors')
    start = datetime.now()
    index_authors(graph, developers, batch_size)
    create_index_authors(graph)
    print('Indexed authors in: \t', datetime.now()-start)

    print('Indexing ', len(commits), ' commits')
    start = datetime.now()
    index_commits(graph, commits, batch_size)
    create_index_commits(graph)
    print('Indexed commits in: \t', datetime.now()-start)

    print('Indexing ', len(dev_commits), ' author_commits')
    start = datetime.now()
    index_author_commits(graph, dev_commits, batch_size)
    print('Indexed author_commits in: \t', datetime.now()-start)

    print('Indexing ', len(branches), ' branches')
    start = datetime.now()
    index_branches(graph, branches, batch_size)
    create_index_branches(graph)
    index_branch_commits(graph, branches_commits, batch_size)
    print('Indexed branches in: \t', datetime.now()-start)

    print('Indexing ', len(files), ' files')
    start = datetime.now()
    index_files(graph, files, batch_size)
    create_index_files(graph)
    print('Indexed files in: \t', datetime.now()-start)

    print('Indexing ', len(commit_files), ' commit_files')
    start = datetime.now()
    index_commit_files(graph, commit_files, batch_size)
    print('Indexed commit_files in: \t', datetime.now()-start)

    print('Indexing ', len(methods), ' methods')
    start = datetime.now()
    index_methods(graph, methods, batch_size)
    create_index_methods(graph)
    print('Indexed methods in: \t', datetime.now()-start)

    print('Indexing ', len(file_methods), ' file_methods')
    start = datetime.now()
    index_file_methods(graph, file_methods, batch_size)
    print('Indexed file_methods in: \t', datetime.now()-start)

    print('Indexing ', len(commit_methods), ' commit_methods')
    start = datetime.now()
    index_commit_method(graph, commit_methods, batch_size)
    print('Indexed commit_methods in: \t', datetime.now()-start)

    print('Indexing took: \t', datetime.now()-total)
