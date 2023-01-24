class HttpException(Exception):
    def __init__(self, message: str,status_code: int):
        self.__message: str = message
        self.__status_code: int = status_code
        super().__init__(message)
    @property
    def message(self):
        return self.__message
    @property
    def status_code(self):
        return self.__status_code