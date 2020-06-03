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
    PROJECT_ID = None
    BATCH_SIZE = 100

    def configure(self, *args, **kwargs):
        self.DB_URL = kwargs['db_url']
        self.PORT = kwargs['port']
        self.DB_USER = kwargs['db_user']
        self.DB_PWD = kwargs['db_pwd']
        self.REPO = kwargs['repo']
        self.START_DATE = kwargs['start_date']
        self.END_DATE = kwargs['end_date']
        self.PROJECT_ID = kwargs['project_id']
        self.BATCH_SIZE = kwargs['batch_size']

    def check_config(self):
        """Checks if the config properties are set and
        raises ValueError if any value misses"""

        if self.DB_URL == "":
            raise ValueError("Database URL is not set.")

        if self.PORT == 0:
            raise ValueError("Database port is not set.")

        if self.DB_USER == "" or self.DB_PWD == "":
            raise ValueError("Database credentials are not set.")
