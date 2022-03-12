from typing import Optional


class CheckTokenModel:
    token: str
    cpfRne: int
    tokenValidated: bool
    errorMessage: Optional[str]

    def __init__(self, token: str, cpfRne: int, tokenValidated: bool, errorMessage: Optional[str]):
        self.token = token
        self.cpfRne = cpfRne
        self.tokenValidated = tokenValidated
        self.errorMessage = errorMessage

    def to_dict(self):
        d = {
            'token': self.token,
            'cpfRne': self.cpfRne,
            'tokenValidated': self.tokenValidated,
        }
        if self.errorMessage is not None:
            d['errorMessage'] = self.errorMessage

        return d