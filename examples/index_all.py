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
"""This module is an example of indexing all data from a repository in Neo4j"""

import argparse
from graphrepo.drillers import Driller


def parse_args():
    """Parse argument"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', default='examples/configs/pydriller.yml', type=str)
    return parser.parse_args()


def main():
    """Main method"""
    args = parse_args()
    driller = Driller(config_path=args.config)
    # this method should be called only once, when initializing
    # a database for the first time
    driller.init_db()
    driller.drill_batch()


if __name__ == '__main__':
    main()
