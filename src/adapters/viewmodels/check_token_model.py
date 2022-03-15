from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class CheckTokenModel():
    role: ROLE
    accesslevel: ACCESS_LEVEL
    cpfRne: int
    email: str
    validToken: bool

    def __init__(self, role: str, accesslevel: str, cpfRne: int, email: str, validToken: bool):
        self.role = role
        self.accesslevel = accesslevel
        self.cpfRne = cpfRne
        self.email = email
        self.validToken = validToken

    @staticmethod
    def fromDict(data: dict):
        return CheckTokenModel(
        role = data['role'],
        accesslevel = data['accessLevel'],
        cpfRne = data['cpfRne'],
        email = data['email'],
        validToken = data['validToken']
        )

    def toDict(self):
        return {
            'role': self.role.value,
            'access_level': self.accesslevel.value,
            'cpf_rne': self.cpfRne,
            'email': self.email,
            'valid_token': self.validToken
        }
