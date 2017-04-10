import time

class Db(dict):
    
    def __init__(self, *args, **kwargs):
        self._meta = dict()
        self._db = dict()

    def __setitem__(self, key, val, ttl=None):
        self._db[key] = val
        self._meta[key] = {
            'created': time.time(),
            'ttl': ttl
        }

    def __getitem__(self, key):
        meta = self._meta[key]
        now = time.time()
        if meta and meta['ttl'] and now > meta['created'] + meta['ttl']:
            del self[key]
        return self._db[key]

    def __delitem__(self, key):
        del self._db[key]
        del self._meta[key]

    def set_ttl(self, key, ttl):
        self._meta[key] = {
            'ttl': ttl,
            'created': time.time()
        }

    def get_ttl(self, key):
        meta = self._meta.get(key)
        return meta['ttl'] if meta else None