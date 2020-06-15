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
    parser.add_argument(
        '--config', default='examples/configs/pydriller.yml', type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    mine_manager = MineManager(config_path=args.config)
    files = mine_manager.dev_miner.get_files(
        "6cf1f138e29c1bf82810ad0b73012302e0d20c2f76a24e3b225017b0",
        mine_manager.config.ct.project_id
    )
    print(len(files), ' files')

    file_updates = mine_manager.dev_miner.get_files_updates(
        "6cf1f138e29c1bf82810ad0b73012302e0d20c2f76a24e3b225017b0",
        mine_manager.config.ct.project_id
    )
    print(len(file_updates), ' file updates')

    methods = mine_manager.dev_miner.get_methods(
        "6cf1f138e29c1bf82810ad0b73012302e0d20c2f76a24e3b225017b0",
        mine_manager.config.ct.project_id
    )
    print(len(methods), ' methods')

    method_updates = mine_manager.dev_miner.get_method_updates(
        "6cf1f138e29c1bf82810ad0b73012302e0d20c2f76a24e3b225017b0",
        mine_manager.config.ct.project_id
    )
    print(len(method_updates), ' method updates')


if __name__ == '__main__':
    main()
