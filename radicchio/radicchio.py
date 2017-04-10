from db import Db

class Radicchio(object):

    db = Db()

    STATUSES = {
        'ok': 'OK',
        'error': 'ERROR'
    }

    MESSAGES = {
        'unknown_command': 'Unknown command',
        'not_an_integer': 'The value is not an integer'
    }

    def handle(self, command, args={}):
        command = command.lower()
        status = self.STATUSES['error']
        result = None
        message = None
        response = dict(status=status)
        try:
            fn = getattr(self, command)
            result = fn(**args)
            status = self.STATUSES['ok']
        except AttributeError:
            message = self.MESSAGES['unknown_command']
        except KeyError:
            if command == 'get':
                status = self.STATUSES['ok']
                response.update(dict(result=None))
        except TypeError:
            if command == 'incr' or command == 'decr':
                response.update(dict(message=self.MESSAGES['not_an_integer']))
        if status == self.STATUSES['error']:
            response.update(dict(message=message))
        elif result is not None:
            response.update(dict(result=result))
        response.update(dict(status=status))
        return response

    def _add(self, key, num):
        try:
            val = self.db[key] + num
            self.db[key] = val
        except KeyError:
            val = 1
            self.db[key] = val
        return val

    def set(self, key, value):
        self.db[key] = value

    def get(self, key):
        return self.db[key]

    def delete(self, key):
        del self.db[key]

    def incr(self, key):
        return self._add(key, +1)

    def decr(self, key):
        return self._add(key, -1)

    def expire(self, key, ttl):
        self.db.set_ttl(key, ttl)
        return ttl