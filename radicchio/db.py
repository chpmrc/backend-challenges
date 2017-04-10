import time
import random

class Db(dict):

    MAX_KEYS = 100

    def __init__(self, *args, **kwargs):
        self._meta = dict()
        self._db = dict()

    def __setitem__(self, key, val):
        self._db[key] = val
        self._meta[key] = {
            'created': time.time(),
            'ttl': None
        }
        self._maintain()

    def __getitem__(self, key):
        now = time.time()
        if self._expired(key):
            del self[key]
        return self._db[key]
        self._maintain()

    def __delitem__(self, key):
        del self._db[key]
        del self._meta[key]
        self._maintain()

    def _expired(self, key):
        meta = self._meta[key]
        ttl = meta.get('ttl')
        created = meta['created']
        now = time.time()
        return ttl and now > created + ttl

    def _maintain(self):
        # Like in Redis: keep evicting expired keys as long as the evicted keys are 25% of the selected ones
        keys = self._db.keys()
        del_count = 0
        if len(keys) > self.MAX_KEYS:
            while del_count == 0 or del_count > self.MAX_KEYS / 4:
                del_count = 0
                now = time.time()
                selected = random.sample(keys, self.MAX_KEYS)
                for s in selected:
                    if self._expired(s):
                        del self[key]
                        del_count += 1

    def set_ttl(self, key, ttl):
        self._meta[key] = {
            'ttl': ttl,
            'created': time.time()
        }

    def get_ttl(self, key):
        meta = self._meta.get(key)
        return meta['ttl'] if meta else None
