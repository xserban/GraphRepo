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
"""Utils methods for GraphRepo"""
import json
import hashlib
from datetime import datetime
import yaml


class Dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def parse_config(path):
    with open(path, 'r') as ymlfile:
        conf = yaml.load(ymlfile, Loader=yaml.FullLoader)

    neo = conf['neo']
    project = conf['project']

    project['start_date'] = datetime.strptime(
        project['start_date'], '%d %B, %Y %H:%M') \
        if project['start_date'] else None
    project['end_date'] = datetime.strptime(
        project['end_date'], '%d %B, %Y %H:%M') \
        if project['end_date'] else None

    return neo, project


def save_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def load_json(path):
    with open(path) as json_file:
        return json.load(json_file)


def get_file_hash(file, project_id=None, use_new_path=False):
    name = ''
    if not file.old_path and file.new_path:
        name = name+file.new_path
    elif file.old_path and not file.new_path:
        name = name+file.old_path
    elif file.old_path and file.new_path:
        if file.old_path != file.new_path:
            print(file.old_path, file.new_path)
        if use_new_path:
            name = name+file.new_path
        else:
            name = name + file.old_path

    name = name+file.filename
    name = project_id + name if project_id else name
    return hashlib.sha224(str(name).encode('utf-8')).hexdigest()


def get_method_type(method, m_before, m_current):
    if method.name in m_before and method.name not in m_current:
        return "DELETE"
    elif method.name in m_before and method.name in m_current:
        return "MODIFY"
    else:
        return "ADD"


def get_method_hash(method, file, project_id=None):
    fhash = get_file_hash(file, project_id)
    _fmname = fhash + "_" + method.long_name
    _fmname = project_id + _fmname if project_id else _fmname
    return hashlib.sha224(_fmname.encode('utf-8')).hexdigest()


def get_author_hash(email):
    return hashlib.sha224(email.encode('utf-8')).hexdigest()


def format_dev(dev, index_email=True):
    return {
        'name': dev.author.name,
        'email': dev.author.email if index_email else '',
        'hash': get_author_hash(dev.author.email)
    }


def get_commit_hash(chash, project_id):
    return hashlib.sha224(str(project_id + chash).encode('utf-8')).hexdigest()


def format_commit(com, project_id):
    return {
        'hash': get_commit_hash(com.hash, project_id),
        'commit_hash': com.hash,
        'message': com.msg,
        'is_merge': 1 if com.merge else 0,
        'timestamp': com.author_date.timestamp(),
        'project_id': project_id,
        'dmm_unit_complexity': com.dmm_unit_complexity if com.dmm_unit_complexity else -1,
        'dmm_unit_interfacing': com.dmm_unit_interfacing if com.dmm_unit_interfacing else -1,
        'dmm_unit_size': com.dmm_unit_size if com.dmm_unit_size else -1,
    }


def format_parent_commit(c_hash, parent_hash, project_id=None):
    return {
        'child_hash': c_hash,
        'parent_hash': get_commit_hash(parent_hash, project_id)
    }


def format_branch(name, project_id):
    return {
        'hash':  hashlib.sha224(str(project_id+name).encode('utf-8')).hexdigest(),
        'project_id': project_id,
        'name': name
    }


def format_author_commit(dev, com, timestamp):
    return {'commit_hash': com['hash'],
            'author_hash': dev['hash'],
            'timestamp': timestamp,
            }


def format_branch_commit(bhash, chash):
    return {'branch_hash': bhash,
            'commit_hash': chash
            }


def format_file(file, project_id):
    return {
        'hash': get_file_hash(file, project_id),
        'new_hash': get_file_hash(file, project_id, use_new_path=True),
        'name': file.filename,
        'project_id': project_id,
        'type': '.' + file.filename.split('.')[-1:][0]
    }


def format_commit_file(c_hash, f_hash, file, timestamp, index_code=True):
    dt_ = {'commit_hash': c_hash, 'file_hash': f_hash,
           'attributes': {
               'timestamp': timestamp,
               'old_path': file.old_path if file.old_path else '',
               'path': file.new_path if file.new_path else '',
               'source_code': '',
               'source_code_before': '',
               'diff': file.diff,
               'nloc': file.nloc if file.nloc else -1,
               'complexity': file.complexity if file.complexity else -1,
               'token_count': file.token_count if file.token_count else -1,
               'added': file.added,
               'removed': file.removed,
               'type': file.change_type.name}}

    if index_code:
        dt_['attributes']['source_code'] = str(
            file.source_code) if file.source_code else '',
        dt_['attributes']['source_code_before'] = str(
            file.source_code_before) if file.source_code_before else '',

    return dt_


def format_commit_method(c_hash, m_hash, met, timestamp):
    return {
        'commit_hash': c_hash,
        'method_hash': m_hash,
        'attributes': {
            'timestamp': timestamp,
            'long_name': met.long_name,
            'parameters': met.parameters,
            'complexity': met.complexity,
            'nloc': met.nloc,
            'fan_in': met.fan_in,
            'fan_out': met.fan_out,
            'general_fan_out': met.general_fan_out,
            'length': met.length,
            'token_count': met.token_count,
            'start_line': met.start_line,
            'end_line': met.end_line}}


def format_method(met, fille, project_id):
    return {
        'hash': get_method_hash(met, fille, project_id),
        'name': met.name,
        'file_name': met.filename,
        'project_id': project_id}


def format_file_method(f_hash, m_hash):
    return {'file_hash': f_hash, 'method_hash': m_hash}
