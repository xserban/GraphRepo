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
because it is used across several modules inside the app"""

from graphrepo.singleton import Singleton
from graphrepo.utils import Dotdict


class Config(metaclass=Singleton):
    """This class contains all config flags"""
    ct = {}

    def configure(self, **kwargs):
        """Stores configuration contants, parsed
        from yaml config file
        :param kwargs: keys and values from config
        """
        self.ct = Dotdict(kwargs)

    def check_config(self):
        """Checks if the config properties are set and
        raises ValueError if any value misses"""

        if not self.ct.db_url or not self.ct.port \
                or not self.ct.db_user or not self.ct.db_pwd:
            raise ValueError("Neo4j configuartion is invalid.")
