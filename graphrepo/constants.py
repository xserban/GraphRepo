""" This mpdule stores all config constants
"""
from datetime import datetime


class Constants(object):
  """ Class with all constants
  """
  DB_URL = 'localhost'
  DB_USER = 'neo4j'
  DB_PWD = 'letmein'
  REPO = 'pydriller/'
  START_DATE = datetime(2018, 12, 1)
  END_DATE = datetime(2019, 1, 1)
