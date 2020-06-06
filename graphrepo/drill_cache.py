from diskcache import Index


class DrillCacheSequential:
    def __init__(self):
        self.data = Index([('commits', []),
                           ('parents', []), ('developers', []),
                           ('dev_commits', []), ('branches', []),
                           ('branches_commits', []), ('files', []),
                           ('commit_files', []), ('methods', []),
                           ('file_methods', []), ('commit_methods', [])
                           ])

    def append_cache(self, key, value):
        temp_ = self.data[key]
        temp_.append(value)
        self.data[key] = temp_
