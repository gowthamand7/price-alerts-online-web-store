
class UserError(Exception):
    def __init__(self,message, code):
        self.message = message
        self.code = code


class UserNotExistsError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass


class UserAlreadyExists(UserError):
    pass


class InvalidInput(UserError):
    pass