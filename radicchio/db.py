class Db(object):
    
    def __init__(self, *args, **kwargs):
        self._db = dict()

    def __setitem__(self, key, val):
        self._db[key] = val

    def __getitem__(self, key):
        return self._db[key]

    def __delitem__(self, key):
        del self._db[key]