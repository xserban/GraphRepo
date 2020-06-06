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
    parser.add_argument('--plot', default=False, type=bool)
    return parser.parse_args()


def main():
    args = parse_args()

    if 'jax' in args.config:
        file_query = {
            'hash': '84a34a3b24d33ba7736a19f7009591d6d4af6aa4368680664fd3a5ae'}

    start = datetime.now()

    mine_manager = MineManager(config_path=args.config)
    updated_file_rels = mine_manager.file_miner.get_change_history(
        file_hash=file_query['hash'])
    complexity = [x['complexity'] for x in updated_file_rels]

    print('File complexity took {}'.format(datetime.now() - start))
    print('File changes', len(updated_file_rels))
    # print(updated_file_rels.data)


if __name__ == '__main__':
    main()
