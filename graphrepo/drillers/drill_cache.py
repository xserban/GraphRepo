"""This module saves the cache data on disk"""
import collections
from diskcache import Index


class DrillCache:
    """Class for storing all data at once in the cache"""

    def __init__(self, data):
        """Transforms dictionary to ordered dic and saves it"""
        dt_ = [(k, v) for k, v in data.items()]
        self.data = Index(collections.OrderedDict(dt_))


class DrillCacheSequential:
    """Class for disk cache sequential"""

    def __init__(self):
        """Init drill cache"""
        self.data = Index([('commits', []),
                           ('parents', []), ('developers', []),
                           ('dev_commits', []), ('branches', []),
                           ('branches_commits', []), ('files', []),
                           ('commit_files', []), ('methods', []),
                           ('file_methods', []), ('commit_methods', [])
                           ])

    def append_cache(self, key, value):
        """Appends record to array on disk ccache
        :param key: data key
        :param value: value to append
        """
        temp_ = self.data[key]
        temp_.append(value)
        self.data[key] = temp_
