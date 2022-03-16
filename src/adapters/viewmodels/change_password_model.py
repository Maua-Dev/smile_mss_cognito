

class ChangePasswordModel():
    result: bool
    message: str

    def __init__(self, result: bool, message: str = None):
        self.result = result
        self.message = message

    @staticmethod
    def fromDict(data: dict):
        return ChangePasswordModel(
            result=data['result'],
            message=data.get('message')
        )

    def toDict(self):
        return {
            'result': self.result,
            'message': self.message if self.message else ''

        }
