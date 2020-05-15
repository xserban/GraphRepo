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

    file_ = node_matcher.match("File", name="commit.py").first()
    methods = [rel.end_node for rel in rel_matcher.graph.match(
        [file_, None], "HasMethod")]
    m_changes = []
    for m in methods:
        changed_rel = list(rel_matcher.graph.match([None, m], "UpdateMethod"))
        mc = [{'complexity': x['complexity'], 'date':  x['author_date'],
               'name': m['name']} for x in changed_rel]
        m_changes = m_changes + mc

    df = pd.DataFrame(m_changes)
    df['date'] = pd.to_datetime(df.date)
    df = df.sort_values(by='date')
    fig = px.line(df, x="date", y="complexity", color="name",
                  line_group="name", hover_name="name")
    fig.show()


if __name__ == '__main__':
    main()
