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

import argparse
import time
import os
import yaml
from graphrepo.driller import Driller
from graphrepo.utils import parse_config
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config.yml', type=str)
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
    driller.drill()
    print('Indexing took {} s.'.format(time.time() - start))


if __name__ == '__main__':
    main()
