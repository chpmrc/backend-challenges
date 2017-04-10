import time
import random
from heapq import *

class Db(dict):

    MAX_KEYS = 100

    def __init__(self, *args, **kwargs):
        self._meta = dict()
        self._db = dict()
        self._accesses = list()

    def __setitem__(self, key, val):
        now = int(time.time())
        self._db[key] = val
        self._meta[key] = {
            'created': now,
            'ttl': None
        }
        self._maintain()

    def __getitem__(self, key):
        now = time.time()
        heappush(self._accesses, (now, key))
        if self._expired(key):
            del self[key]
        return self._db[key]
        self._maintain()

    def __delitem__(self, key):
        del self._db[key]
        del self._meta[key]

    def _expired(self, key):
        meta = self._meta[key]
        ttl = meta.get('ttl')
        created = meta['created']
        now = time.time()
        return ttl and now > created + ttl

    def _maintain(self):
        # Use a priority queue to run eviction in Om(log(n))
        key_count = self.key_count()
        if key_count > self.MAX_KEYS:
            to_evict_count = key_count - int(self.MAX_KEYS / 2)
            items = nsmallest(to_evict_count, self._accesses) if to_evict_count > 0 else []
            for i in items:
                key = i[1]
                try:
                    del self[key]
                except KeyError:
                    pass  # A duplicate
            self._accesses = self._accesses[to_evict_count:]

    def set_ttl(self, key, ttl):
        self._meta[key] = {
            'ttl': ttl,
            'created': time.time()
        }

    def get_ttl(self, key):
        meta = self._meta.get(key)
        return meta['ttl'] if meta else None

    def key_count(self):
        return len(self._db.keys())