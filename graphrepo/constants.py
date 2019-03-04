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

""" This mpdule stores all config constants
"""
from datetime import datetime


class Constants(object):
  """ Class with all constants
  """
  DB_URL = 'localhost'
  PORT = 13000
  DB_USER = 'neo4j'
  DB_PWD = 'letmein'
  REPO = 'pydriller/'
  START_DATE = datetime(2018, 12, 1)
  END_DATE = datetime(2019, 1, 1)
  # START_DATE = None
  # END_DATE = None
