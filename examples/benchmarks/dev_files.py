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

    if 'jax' in args.config:
        dev_query = {
            'hash': '93476add93abfb4fcfdd5c61ed811099bbb2aab70874f554d38bf381'}

    start = datetime.now()
    mine_manager = MineManager(config_path=args.config)
    files = mine_manager.dev_miner.get_files(
        dev_query['hash'],
        mine_manager.config.ct.project_id
    )
    ft = [f['type'] for f in files]
    grouped = [{'file': x, 'count': len(
        [y for y in ft if x == y])} for x in set(ft)]

    print('Dev file types took {}'.format(datetime.now() - start))
    print('Nr files', len(ft))


if __name__ == '__main__':
    main()
