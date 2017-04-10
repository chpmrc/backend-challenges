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
        heappush(self._accesses, (now, key))
        self._maintain()

    def __getitem__(self, key):
        now = time.time()
        self._meta[key]['last_access'] = now
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
        to_evict_count = self.key_count() - self.MAX_KEYS
        items = nlargest(self._accesses, to_evict_count) if to_evict_count > 0 else []
        for i in items:
            key = i[1]
            del self[key]

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