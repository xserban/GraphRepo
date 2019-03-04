""" This module uses pydriller to search a repository
and indexes it in neo4j
"""
from pydriller import RepositoryMining, GitRepository
from constants import Constants
from models import Commit, File, Developer

CT = Constants()


class Driller(object):
  """ Drill class - parses a git repo and uses the models
  to index everything in Neo4j
  """

  def __init__(self):
    pass

  def drill(self, repo=CT.REPO):
    """ Method to index the repo in neo4j
    :param repo: a constant
    """
    rep_obj = GitRepository(repo)
    commits = []
    for commit in RepositoryMining(repo, since=CT.START_DATE, to=CT.END_DATE).traverse_commits():
      commits.append(Commit(commit))
    return commits, rep_obj
