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
import yaml
import hashlib
from datetime import datetime


def parse_config(path):
    with open(path, 'r') as ymlfile:
        conf = yaml.load(ymlfile, Loader=yaml.FullLoader)

    neo = conf['neo']
    project = conf['project']

    project['start_date'] = datetime.strptime(
        project['start_date'], '%d %B, %Y %H:%M') if project['start_date'] else None
    project['end_date'] = datetime.strptime(
        project['end_date'], '%d %B, %Y %H:%M') if project['end_date'] else None

    return neo, project


def get_day_hash(date):
    return hashlib.sha224(
        (str(date.month) + str(date.year)
         + str(date.day)).encode('utf-8')).hexdigest()


def get_month_hash(date):
    return hashlib.sha224(
        (str(date.month) + str(date.year)).encode('utf-8')).hexdigest()


def get_file_hash_neo(file):
    n = ''
    if file['old_path'] and not file['path']:
        n = n+file['old_path']
    else:
        n = n+file['path']

    n = n+file['name']
    return hashlib.sha224(str(n).encode('utf-8')).hexdigest()


def get_file_hash(file):
    n = ''
    if file.old_path and not file.new_path:
        n = n+file.old_path
    else:
        n = n+file.new_path

    n = n+file.filename
    return hashlib.sha224(str(n).encode('utf-8')).hexdigest()


def get_file_type_hash(name):
    return hashlib.sha224(str(name).encode('utf-8')).hexdigest()


def get_method_hash(method, file):
    try:
        fhash = get_file_hash(file)
    except Exception as e:
        fhash = get_file_hash_neo(file)
    _fmname = fhash + "_" + method.name
    return hashlib.sha224(_fmname.encode('utf-8')).hexdigest()


def get_file_attributes(file):
    return {
        'old_path': file.old_path if file.old_path else '',
        'path': file.new_path if file.new_path else '',
        'source_code': file.source_code if file.source_code else '',
        'source_code_before':  file.source_code_before if file.source_code_before else '',
        'nloc': file.nloc if file.nloc else -1,
        'complexity': file.complexity if file.complexity else -1,
        'token_count': file.token_count if file.token_count else -1,
    }


def get_file_change(file):
    return str(file.change_type).split(".")[1]


def update_file_attributes(changes, change_type, file, graph):
    for k, v in changes.items():
        file[k] = v
    file['type'] = change_type
    graph.push(file)


def get_file_metrics(file):
    return {
        'added': file.added,
        'removed': file.removed,
        'type': file.change_type.name,
    }


def get_method_metrics(method):
    return {
        'parameters': method.parameters,
        'complexity': method.complexity,
        'nloc': method.nloc,
        'fan_in': method.fan_in,
        'fan_out': method.fan_out,
        'general_fan_out': method.general_fan_out,
        'length': method.length,
        'token_count': method.token_count,
        'start_line': method.start_line,
        'end_line': method.end_line
    }


def update_method_attributes(metrics, node, graph):
    for k, v in metrics.items():
        node[k] = v
    graph.push(node)


def get_method_type(method, m_before, m_current):
    if method.name in m_before and method.name not in m_current:
        return "DELETE"
    elif method.name in m_before and method.name in m_current:
        return "MODIFY"
    else:
        return "ADD"


def get_file_hash(file):
    n = ''
    if file.old_path and not file.new_path:
        n = n+file.old_path
    else:
        n = n+file.new_path

    n = n+file.filename
    return hashlib.sha224(str(n).encode('utf-8')).hexdigest()


def get_method_hash(method, file):
    fhash = get_file_hash(file)
    _fmname = fhash + "_" + method.long_name
    return hashlib.sha224(_fmname.encode('utf-8')).hexdigest()


def get_author_hash(email):
    return hashlib.sha224(email.encode('utf-8')).hexdigest()


def format_dev(a):
    return {
        'name': a.author.name,
        'email': a.author.email,
        'hash': get_author_hash(a.author.email)
    }


def format_commit(c, project_id):
    return {
        'hash': c.hash,
        'is_merge': 1 if c.merge else 0,
        'timestamp': c.author_date.timestamp(),
        'project_id': project_id
    }


def format_branch(name, project_id):
    return {
        'hash':  hashlib.sha224(str(name).encode('utf-8')).hexdigest(),
        'project_id': project_id,
        'name': name
    }


def format_author_commit(a, c, timestamp):
    return {'commit_hash': c['hash'],
            'author_hash': a['hash'],
            'timestamp': timestamp,
            }


def format_branch_commit(b, c):
    return {'branch_hash': b, 'commit_hash': c}


def format_file(f, project_id):
    return {
        'hash': get_file_hash(f),
        'name': f.filename,
        'project_id': project_id,
        'type': '.' + f.filename.split('.')[-1:][0]
    }


def format_commit_file(c_hash, f_hash, f, timestamp):
    return {'commit_hash': c_hash, 'file_hash': f_hash,
            'attributes': {
                'timestamp': timestamp,
                'old_path': f.old_path if f.old_path else '',
                'path': f.new_path if f.new_path else '',
                'source_code': str(f.source_code) if f.source_code else '',
                'source_code_before':  str(f.source_code_before) if f.source_code_before else '',
                'nloc': f.nloc if f.nloc else -1,
                'complexity': f.complexity if f.complexity else -1,
                'token_count': f.token_count if f.token_count else -1,
                'added': f.added,
                'removed': f.removed,
                'type': f.change_type.name}
            }


def format_commit_method(c_hash, m_hash, m, timestamp):
    return {
        'commit_hash': c_hash,
        'method_hash': m_hash,
        'attributes': {
            'timestamp': timestamp,
            'long_name': m.long_name,
            'parameters': m.parameters,
            'complexity': m.complexity,
            'nloc': m.nloc,
            'fan_in': m.fan_in,
            'fan_out': m.fan_out,
            'general_fan_out': m.general_fan_out,
            'length': m.length,
            'token_count': m.token_count,
            'start_line': m.start_line,
            'end_line': m.end_line
        }
    }


def format_method(m, f, project_id):
    return {
        'hash': get_method_hash(m, f),
        'name': m.name,
        'file_name': m.filename,
        'project_id': project_id
    }


def format_file_method(f_hash, m_hash):
    return {'file_hash': f_hash, 'method_hash': m_hash}
