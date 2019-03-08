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

"""This module stores all config constants. It is a singleton
because it is used across in several modules inside the app"""

from graphrepo.singleton import Singleton


class Config(metaclass=Singleton):
  """This class contains all config flags"""
  DB_URL = ""
  PORT = 0
  DB_USER = ""
  DB_PWD = ""
  REPO = ""
  START_DATE = None
  END_DATE = None
  # If True, each branch will be indexed as a node
  # and commits will be linked by a Parent relationship
  # If False, then the commits are linked by a Branch
  # relationship
  BRANCH_AS_NODE = True

  def check_config(self):
    """Checks if the config properties are set and
    raises ValueError if any value misses"""

    if self.DB_URL == "":
      raise ValueError("Database URL is not set.")

    if self.PORT == 0:
      raise ValueError("Database port is not set.")

    if self.DB_USER == "" or self.DB_PWD == "":
      raise ValueError("Database credentials are not set.")

    if self.REPO == "":
      raise ValueError("Repository path not set.")
