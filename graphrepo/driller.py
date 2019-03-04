# Copyright 2019 NullConvergence
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

""" This module uses pydriller to search a repository
and indexes it in neo4j
"""
from pydriller import RepositoryMining, GitRepository
from graphrepo.constants import Constants
from graphrepo.models.commit import Commit

CT = Constants()


class Driller(object):
  """ Drill class - parses a git repo and uses the models
  to index everything in Neo4j
  """

  def __init__(self):
    pass

  def drill(self, repo=CT.REPO):
    """ Method to index the repo in neo4j
    :param repo: a string with the repo path
    """
    rep_obj = GitRepository(repo)
    commits = []
    for commit in RepositoryMining(repo, since=CT.START_DATE, to=CT.END_DATE).traverse_commits():
      commits.append(Commit(commit))
    return commits, rep_obj
