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
# This file assumes the project from the config file was already indexed
###
import argparse
import os
import pandas as pd
import plotly.express as px

from datetime import datetime
from graphrepo.miners import MineManager
from graphrepo.utils import parse_config


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='configs/pydriller.yml', type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    mine_manager = MineManager(config_path=args.config)

    file_miner = mine_manager.file_miner
    file_ = file_miner.query(pproject_id=mine_manager.config.ct.project_id,
                             name="commit.py")
    updated_file_rels = file_miner.get_change_history(file_['hash'])

    # sort update relationships and transform data for plotting
    updated_file_rels.sort(key=lambda x: x['timestamp'])

    complexity = [x['complexity'] for x in updated_file_rels]
    nloc = [x['nloc'] for x in updated_file_rels]
    dts = [datetime.fromtimestamp(x['timestamp']) for x in updated_file_rels]

    fig = px.line(pd.DataFrame({'date': dts, 'complexity': complexity}),
                  x='date', y='complexity',
                  title='Complexity over time for the commit.py file')
    fig.show()

    fig_2 = px.line(pd.DataFrame({'date': dts, 'nloc': nloc}),
                    x='date', y='nloc', title="NLOC over time for the commit.py file")
    fig_2.show()


if __name__ == '__main__':
    main()
