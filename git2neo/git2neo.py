#!/usr/bin/env python

from __future__ import print_function

from collections import namedtuple
from itertools import tee
from operator import itemgetter
from subprocess import Popen, PIPE
import re

Commit = namedtuple('Commit', ['sha1', 'hash', 'parents', 'author_email',
                               'author_name', 'refs', 'subject', 'timestamp', 'date_time'])
GIT_LOG_FORMAT = '%x1E'.join(
    ['%H', '%h', '%P', '%ae', '%an', '%d', '%s', '%at', '%ai'])

seen_sha1s = set()


def as_list(elements):
  items = [e for e in elements if e]
  return items or None


def fix_parents(parents_string):
  return as_list(parents_string.split())


def fix_refs(refs_string):
  return as_list(refs_string.strip()[1:-1].split(', '))


def mk_commit(commit_line):
  commit_line = re.sub(r'[^\x00-\x7F]+', '', commit_line)
  commit = Commit(*commit_line.split('\x1E'))
  parents = fix_parents(commit.parents)
  refs = fix_refs(commit.refs)
  return commit._replace(parents=parents, refs=refs)


def create_node(neo4j_op, sha1_ident, property_pairs):
  if property_pairs:
    properties = ','.join('{0}:{1!r}'.format(k, v)
                          for k, v in property_pairs)
    return neo4j_op + ' (:Commit {{{0}}});'.format(properties)
  else:
    return neo4j_op + ' (:Commit);'


def create_rel(neo4j_op, sha1, parent):
  return 'MATCH (parent:Commit {sha1:"'+sha1+'"}), (child:Commit {sha1:"'+parent+'"}) '+neo4j_op+' (parent)<-[:PARENT]-(child);'


def mk_node_stmts(neo4j_op, sha1_ident, **properties):
  if sha1_ident not in seen_sha1s:
    seen_sha1s.add(sha1_ident)
    props = {k: v for k, v in properties.iteritems() if v is not None}
    yield create_node(neo4j_op, sha1_ident, sorted(props.items(), key=itemgetter(0)))


def node_stmts(neo4j_op, commit_or_sha1):
  if (hasattr(commit_or_sha1, 'sha1')):
    sha1, properties = (commit_or_sha1.sha1, commit_or_sha1._asdict())
  else:
    sha1, properties = (commit_or_sha1, {})
  return mk_node_stmts(neo4j_op, sha1, **properties)


def nodes(neo4j_op, cs):
  for c in cs:
    for s in node_stmts(neo4j_op, c):
      yield s


def missing_parents(neo4j_op, parents):
  for parent in parents or []:
    for n in node_stmts(neo4j_op, parent):
      yield n


def rel_stmts(neo4j_op, sha1, parents):
  for parent in parents or []:
    yield create_rel(neo4j_op, sha1, parent)


def join_rel_stmts(neo4j_op, cs):
  it = (s for c in cs for s in rel_stmts(neo4j_op, c.sha1, c.parents))
  a, b = tee(it)
  next(b, None)
  for _ in b:
    yield next(a)
  yield next(a)


def rels(neo4j_op, cs):
  for c in cs:
    for s in missing_parents(neo4j_op, c.parents):
      yield s
  for s in join_rel_stmts(neo4j_op, cs):
    yield '  ' + s


def mk_cmd(limit, branch):
  git_log = ['git', 'log', '--format=format:{0}'.format(GIT_LOG_FORMAT)]
  if limit is not None:
    git_log.append('-n')
    git_log.append(str(limit))
  if branch is not None:
    git_log.append(str(branch))
  return git_log


def commits(limit, branch):
  proc = Popen(mk_cmd(limit, branch), stdout=PIPE)
  for line in proc.stdout:
    yield line.strip()


def main(neo4j_op, limit=None, branch=None):
  cs = map(mk_commit, commits(limit, branch))
  statements = []
  if cs:
    statements.append('BEGIN')
    statements.extend(nodes(neo4j_op, cs))
    statements.append('COMMIT')
    statements.append('BEGIN')
    statements.append(
        'MATCH (n:Commit) SET n.date = substring(n.date_time,0,10);')
    statements.append('COMMIT')
    statements.append('BEGIN')
    statements.append('create index on :Commit(hash);')
    statements.append('create index on :Commit(author_name);')
    statements.append('create index on :Commit(author_email);')
    statements.append('create index on :Commit(date);')
    statements.append(
        'create constraint on (c:Commit) assert c.sha1 is unique;')
    statements.append('COMMIT')
    statements.append('BEGIN')
    if len(cs) > 1:
      statements.extend(rels(neo4j_op, cs))
    statements.append('COMMIT')
  return statements


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', '--limit', type=int, metavar='N',
                      help='only N latest commits', default=None)
  parser.add_argument('--merge', dest='neo4j_op', const='MERGE', default='CREATE',
                      action='store_const', help='use MERGE instead of CREATE')
  parser.add_argument('--json', action='store_true',
                      help='print JSON output for the Cypher REST API.')
  parser.add_argument(
      'branch', help='which branch to examine - defaults to HEAD', nargs='?', default=None)
  arguments = parser.parse_args()
  res = main(arguments.neo4j_op, arguments.limit, arguments.branch)
  if arguments.json:
    import json
    import sys
    json.dump({"query": ' '.join(res)}, sys.stdout)
  else:
    print('\n'.join(res))
