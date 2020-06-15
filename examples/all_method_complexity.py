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
"""This module plots the method complexity evolution over time, for a file"""

###
# This file assumes the project from the config file was already indexed
###
import argparse
import pandas as pd
import plotly.express as px

from graphrepo.miners import MineManager

from datetime import datetime


def parse_args():
    """Parse args"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', default='examples/configs/pydriller.yml', type=str)
    parser.add_argument('--plot', default=False, type=bool)
    return parser.parse_args()


def main():
    """Main"""
    args = parse_args()

    file_query = {
        'hash': 'e2eb7bf414cebe68f46fa88e4abe9ae5813e91c4e1e97570f8e41cf4'}

    start = datetime.now()
    mine_manager = MineManager(config_path=args.config)

    methods = mine_manager.file_miner.get_current_methods(file_query['hash'])

    m_changes = []
    for m in methods:
        changes = mine_manager.method_miner.get_change_history(m)
        mc = [{'complexity': x['complexity'],
               'date':  datetime.fromtimestamp(x['timestamp']),
               'name': m['name']} for x in changes]
        m_changes = m_changes + mc
    print('All methods complexity took: {}'.format(datetime.now() - start))
    print('Total methods: ', len(methods))

    if args.plot:
        df = pd.DataFrame(m_changes)
        df['date'] = pd.to_datetime(df.date)
        df = df.sort_values(by='date')
        fig = px.line(df, x="date", y="complexity", color="name",
                      line_group="name", hover_name="name")
        fig.show()


if __name__ == '__main__':
    main()
