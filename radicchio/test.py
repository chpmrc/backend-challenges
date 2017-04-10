import unittest
import time
from radicchio import Radicchio


class TestRadicchio(unittest.TestCase):

    def setUp(self):
        self.r = Radicchio()
        payload = {
            'command': 'SET',
            'args': {
                'key': 'a',
                'value': 1
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')
        payload.update(dict(args={'key': 'b', 'value': 'c'}))
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')

    def test_get(self):
        payload = {
            'command': 'GET',
            'args': {
                'key': 'a'
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['result'], 1)
        # Try with a non-existing key
        payload.update({'args': {'key': '1234'}})
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['result'], None)

    def test_delete(self):
        payload = {
            'command': 'DELETE',
            'args': {
                'key': 'a'
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')

    def test_incr(self):
        payload = {
            'command': 'INCR',
            'args': {
                'key': 'a'
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['result'], 2)
        payload.update(dict(args={'key': 'b'}))
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'ERROR')  # Not an integer

    def test_expire(self):
        payload = {
            'command': 'EXPIRE',
            'args': {
                'key': 'a',
                'ttl': 1
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')
        time.sleep(1)
        payload.update(dict(command='GET', args={'key': 'a'}))
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['result'], None)


if __name__ == '__main__':
    unittest.main()