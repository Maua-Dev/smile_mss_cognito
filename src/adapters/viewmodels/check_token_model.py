from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class CheckTokenModel():
    role: ROLE
    accesslevel: ACCESS_LEVEL
    cpfRne: int
    email: str

    def __init__(self, role: str, accesslevel: str, cpfRne: int, email: str):
        self.role = role
        self.accesslevel = accesslevel
        self.cpfRne = cpfRne
        self.email = email

    @staticmethod
    def fromDict(data: dict):
        return CheckTokenModel(
        role = data['role'],
        accesslevel = data['accessLevel'],
        cpfRne = data['cpfRne'],
        email = data['email']
        )

    def toDict(self):
        return {
            'role': self.role.value,
            'access_level': self.accesslevel.value,
            'cpf_rne': self.cpfRne,
            'email': self.email
        }
