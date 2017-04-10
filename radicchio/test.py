import unittest
import time
import mock
from radicchio import Radicchio


mock_time = mock.Mock()

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
        self.assertEqual(response['status'], 'OK', response.get('message'))
        payload.update(dict(args={'key': 'b', 'value': 'c'}))
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))

    def test_get(self):
        payload = {
            'command': 'GET',
            'args': {
                'key': 'a'
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))
        self.assertEqual(response['result'], 1)
        # Try with a non-existing key
        payload.update({'args': {'key': '1234'}})
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))
        self.assertEqual(response['result'], None)

    def test_delete(self):
        payload = {
            'command': 'DELETE',
            'args': {
                'key': 'a'
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))

    def test_incr(self):
        payload = {
            'command': 'INCR',
            'args': {
                'key': 'a'
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))
        self.assertEqual(response['result'], 2)
        payload.update(dict(args={'key': 'b'}))
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'ERROR')  # Not an integer

    @mock.patch('time.time', mock_time)
    def test_expire(self):
        mock_time.return_value = 1000
        payload = {
            'command': 'EXPIRE',
            'args': {
                'key': 'a',
                'ttl': 1
            }
        }
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))
        payload.update(dict(command='GET', args={'key': 'a'}))
        mock_time.return_value = 2000
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))
        self.assertEqual(response['result'], None)

    def test_ttl(self):
        payload = {
            'command': 'EXPIRE',
            'args': {
                'key': 'a',
                'ttl': 1
            }
        }
        response = self.r.handle(**payload)
        del payload['args']['ttl']
        payload.update(dict(command='TTL'))
        response = self.r.handle(**payload)
        self.assertEqual(response['status'], 'OK', response.get('message'))
        self.assertEqual(response['result'], 1)

    def test_purge(self):
        payload = {
            'command': 'SET'
        }
        count_payload = {
            'command': 'COUNT'
        }
        for i in range(999):  # There's already an item
            payload.update(dict(args={'key': str(i), 'value': i}))
            self.r.handle(**payload)
        res = self.r.handle(**count_payload)
        self.assertTrue(res['result'] < 100, res['result'])
        payload.update(dict(args={'key': str(100), 'value': 100}))
        self.r.handle(**payload)
        res = self.r.handle(**count_payload)
        self.assertTrue(res['result'] < 100, res['result'])


if __name__ == '__main__':
    unittest.main()