class Radicchio(object):

    db = dict()

    STATUSES = {
        'ok': 'OK',
        'error': 'ERROR'
    }

    MESSAGES = {
        'unknown_command': 'Unknown command'
    }

    def handle(self, command, args={}):
        status = self.STATUSES['error']
        result = None
        message = None
        response = dict(status=status)
        try:
            fn = getattr(self, command.lower())
            result = fn(**args)
            status = self.STATUSES['ok']
        except AttributeError:
            message = self.MESSAGES['unknown_command']
        if status == self.STATUSES['error']:
            response.update(dict(message=message))
        elif result is not None:
            response.update(dict(result=result))
        response.update(dict(status=status))
        return response

    def set(self, key, value):
        self.db[key] = value