

class Radicchio(object):

    ERROR_STATUS = 'error'
    OK_STATUS = 'ok'

    def handle(self, command, args={}):
        status = self.OK_STATUS
        result = None
        try:
            fn = getattr(self, command.lower())
            result = fn(**args)
        except AttributeError:
            status = self.ERROR_STATUS
        return {
            'status': status,
            'result': result
        }

    def set(self, key, value):
        return 'hello'
