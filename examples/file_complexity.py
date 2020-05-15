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


###
# !!! This file uses the pydriller repo and assumes the repo is already indexed in Neo4j
# If it is not indexed, please run 'index_all.py' before with the pydriller config
###
import argparse
import yaml
import time
import os
import pandas as pd
import plotly.express as px

from datetime import datetime
from py2neo import NodeMatcher, RelationshipMatcher
from graphrepo.driller import Driller
from graphrepo.utils import parse_config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/pydriller.yml', type=str)
    return parser.parse_args()


def main():
    start = time.time()
    args = parse_args()
    folder = os.path.dirname(os.path.abspath(__file__))
    neo, project = parse_config(os.path.join(folder, args.config))

    driller = Driller()
    driller.configure(
        **neo, **project
    )
    driller.connect()

    node_matcher = NodeMatcher(driller.graph)
    rel_matcher = RelationshipMatcher(driller.graph)

    # This query can also be implemented faster, but this is an
    # educational example
    # get file
    file_ = node_matcher.match("File", name="commit.py").first()
    # get update file relationships and plot evolution
    updated_file_rels = list(rel_matcher.match([None, file_], "UpdateFile"))
    # sort update relationships
    updated_file_rels.sort(key=lambda x: datetime.strptime(
        x['author_datetime'], "%Y/%m/%d, %H:%M:%S"))
    # get complexity and nloc to plot
    complexity = [x['complexity'] for x in updated_file_rels]
    nloc = [x['nloc'] for x in updated_file_rels]
    dts = [x['author_datetime'] for x in updated_file_rels]

    fig = px.line(pd.DataFrame({'date': dts, 'complexity': complexity}),
                  x='date', y='complexity',
                  title='Complexity over time for the commit.py file')
    fig.show()

    fig_2 = px.line(pd.DataFrame({'date': dts, 'nloc': nloc}),
                    x='date', y='nloc', title="NLOC over time for the commit.py file")
    fig_2.show()


if __name__ == '__main__':
    main()
