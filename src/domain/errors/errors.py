class BaseError(Exception):
    def __init__(self, message: str):
        self.__message: str = message
        super().__init__(message)

    @property
    def message(self):
        return self.__message


class EntityError(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Field {message} is not valid.')

class UnexpectedError(BaseError):
    def __init__(self, message: str, cause: str):
        super().__init__(f'Usecase {message} have failed. {cause}')

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Usecase {message} have failed. No items found')

class UserAlreadyExists(BaseError):
    def __init__(self, message: str):
        super().__init__(f'User already exists. Message: {message}')

class NonExistentUser(BaseError):
    def __init__(self, message: str):
        super().__init__(f'User not found. Message: {message}')

class IncompleteUser(BaseError):
    def __init__(self, message: str):
        super().__init__(f'User missing information. Message: {message}')

class InvalidCode(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Invalid code. Message: {message}')

class InvalidCredentials(BaseError):
    def __init__(self, message: str):
        super().__init__(f'Invalid credentials. Message: {message}')