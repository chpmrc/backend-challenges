import unittest
from radicchio import Radicchio


class TestRadicchio(unittest.TestCase):

    def setUp(self):
        self.r = Radicchio()
        payload = {
            'command': 'SET',
            'args': {
                'key': 'a',
                'value': 'b'
            }
        }
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
        self.assertEqual(response['result'], 'b')
        # Try with a non-existing key
        payload.update({'args': {'key': 'b'}})
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


if __name__ == '__main__':
    unittest.main()