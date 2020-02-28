# Copyright 2020 NullConvergence
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

from py2neo import Graph
from graphrepo.config import Config
from graphrepo.logger import Logger
from graphrepo.singleton import Singleton
from graphrepo import miners


LG = Logger()


class MineManager():
  """MineManageer class - This class manages custom
  miners. For At the moment we instantiate all miners,
  but other managers which handle different teams of miners
  can be created.
  """

  def __init__(self, graph):
    """Initializes the properties of this class"""
    self.graph = graph
    self.init_miners()

  def init_miners(self):
    """Initializes all miners"""
    try:
      # TODO: Maybe make this more automatic
      self.commit_miner = miners.CommitMiner(graph=self.graph)
      self.dev_miner = miners.DeveloperMiner(graph=self.graph)
      self.file_miner = miners.FileMiner(graph=self.graph)
    except Exception as exc:
      LG.log_and_raise(exc)
    else:
      return
