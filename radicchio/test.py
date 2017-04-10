import unittest
from radicchio import Radicchio


class TestRadicchio(unittest.TestCase):

    def setUp(self):
        self.r = Radicchio()

    def test_set(self):
        payload = {
            'command': 'SET',
            'args': {
                'key': 'a',
                'value': 'b'
            }
        }
        response = self.r.handle(**payload)
        assert response['status'] == 'OK'

    def test_get(self):
        payload = {
            'command': 'SET',
            'args': {
                'key': 'a',
                'value': 'b'
            }
        }
        self.r.handle(**payload)
        payload = {
            'command': 'GET',
            'args': {
                'key': 'a'
            }
        }
        response = self.r.handle(**payload)
        assert response['status'] == 'OK'
        assert response['result'] == 'b'
        # Try with a non-existing key
        payload.update({'args': {'key': 'b'}})
        response = self.r.handle(**payload)
        assert response['status'] == 'OK'
        assert response['result'] is None


if __name__ == '__main__':
    unittest.main()