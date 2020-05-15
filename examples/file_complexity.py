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
from graphrepo.miner import Miner
from graphrepo.utils import parse_config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/pydriller.yml', type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    folder = os.path.dirname(os.path.abspath(__file__))
    neo, _ = parse_config(os.path.join(folder, args.config))

    miner = Miner()
    miner.configure(
        **neo
    )

    file_miner = miner.manager.file_miner
    file_ = file_miner.query(name="commit.py")
    updated_file_rels = file_miner.get_change_history(file_)

    # sort update relationships and transform data for plotting
    updated_file_rels.sort(key=lambda x: datetime.strptime(
        x['author_datetime'], "%Y/%m/%d, %H:%M:%S"))

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
