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
"""Logger"""
from graphrepo.singleton import Singleton


class Logger(metaclass=Singleton):
  def __init__(self, *args, **kwargs):
    """Default init"""

  def log(self, exception):
    """Logs exceptions and prints it to console
    :param exception: Exception type from Python
    """
    print('[EXCEPTION]: {}'.format(exception))

  def log_and_raise(self, exception):
    """Logs, prints and raises exception
    :param exception: Python Exception object
    """
    self.log(exception)
    raise exception
