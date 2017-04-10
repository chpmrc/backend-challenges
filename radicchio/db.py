import time

class Db(dict):
    
    def __init__(self, *args, **kwargs):
        self._meta = dict()
        self._db = dict()

    def __setitem__(self, key, val):
        self._db[key] = val

    def __getitem__(self, key):
        meta = self._meta.get(key)
        now = time.time()
        if meta and now > meta['created'] + meta['ttl']:
            del self[key]
        return self._db[key]

    def __delitem__(self, key):
        del self._db[key]
        try:
            del self._meta[key]
        except KeyError:
            pass

    def set_ttl(self, key, ttl):
        self._meta[key] = {
            'ttl': ttl,
            'created': time.time()
        }

    def get_ttl(self, key):
        meta = self._meta.get(key)
        return meta['ttl'] if meta else None