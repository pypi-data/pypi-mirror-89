# Error Class


class ServerError(RuntimeError):
    pass


class BadRequest(RuntimeError):
    pass


class NotFound(RuntimeError):
    pass


class IllegalArgument(RuntimeError):
    pass
