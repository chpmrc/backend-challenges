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


if __name__ == '__main__':
    unittest.main()