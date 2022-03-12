from typing import Optional


class CheckTokenModel:
    token: str
    cpfRne: int
    tokenValidated: bool
    errorMessage: str

    def __init__(self, token: str, cpfRne: int, tokenValidated: bool, errorMessage: str = None):
        self.token = token
        self.cpfRne = cpfRne
        self.tokenValidated = tokenValidated
        self.errorMessage = errorMessage

    def to_dict(self):
        return {
            'token': self.token,
            'cpfRne': self.cpfRne,
            'tokenValidated': self.tokenValidated,
            'errorMessage': self.errorMessage
        }

