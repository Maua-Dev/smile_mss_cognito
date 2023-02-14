

class ConfirmChangePasswordViewmodel():
    result: bool
    message: str

    def __init__(self, result: bool, message: str = None):
        self.result = result
        self.message = message

    @staticmethod
    def from_dict(data: dict):
        return ConfirmChangePasswordViewmodel(
            result=data['result'],
            message=data.get('message')
        )

    def to_dict(self):
        return {
            'result': self.result,
            'message': self.message if self.message else ''
        }
