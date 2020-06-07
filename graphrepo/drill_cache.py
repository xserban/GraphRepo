"""This module saves the cache data on disk"""
from diskcache import Index


class DrillCacheSequential:
    """Class for disk cache"""

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
