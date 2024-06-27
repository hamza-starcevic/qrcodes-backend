class BackendError(Exception):
    pass


class HAAAMUserAlreadyExists(BackendError):
    def __init__(self, msg):
        self.msg = msg


class HAAAMUserDoesNotExist(BackendError):
    def __init__(self, msg):
        self.msg = msg


class HAAAMUserNotAuthorized(BackendError):
    def __init__(self, msg):
        self.msg = msg


class HAAMGenericError(BackendError):
    def __init__(self, msg):
        self.msg = msg
