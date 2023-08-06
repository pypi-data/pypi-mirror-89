class RequestError(Exception):
    def __init__(self, message):
        super(RequestError, self).__init__(message)