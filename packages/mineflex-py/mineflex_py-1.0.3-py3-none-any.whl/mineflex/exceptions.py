class MineflexException(Exception):
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)


class UserException(MineflexException):
    pass


class APIMissingException(MineflexException):
    pass


class InsufficientPermissions(MineflexException):
    pass


class UnknownException(MineflexException):
    pass


class ServerException(MineflexException):
    pass


class InvalidCredentials(MineflexException):
    pass


class ServerOfflineException(ServerException):
    pass
