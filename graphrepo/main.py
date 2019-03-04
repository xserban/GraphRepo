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

from py2neo import Graph
from graphrepo.constants import Constants
from graphrepo.driller import Driller

CT = Constants()

def init_graph():
  """Configures the graph + connection
  :returns: graph
  """
  repo_graph = Graph(host=CT.DB_URL, user=CT.DB_USER, password=CT.DB_PWD, http_port=CT.PORT)
  return repo_graph

def main():
  repo_graph = init_graph()
  driller = Driller()
  commits, repo = driller.drill()

  # index in neo4j
  for com in commits:
    com.index_all_data(repo_graph, repo)

if __name__ == '__main__':
  main()
