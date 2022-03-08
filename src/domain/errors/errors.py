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