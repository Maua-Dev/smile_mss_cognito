from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class LoginUserModel():
    accessToken: str
    refreshToken: str
    role: ROLE
    accesslevel: ACCESS_LEVEL
    cpfRne: int
    email: str

    def __init__(self, accessToken: str, refreshToken: str, role: str, accesslevel: str, cpfRne: int, email: str):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.role = role
        self.accesslevel = accesslevel
        self.cpfRne = cpfRne
        self.email = email

    @staticmethod
    def fromDict(data: dict):
        return LoginUserModel(
        accessToken = data['accessToken'],
        refreshToken = data['refreshToken'],
        role = data['role'],
        accesslevel = data['accessLevel'],
        cpfRne = data['cpfRne'],
        email = data['email']
        )

    def toDict(self):
        return {
            'access_token': self.accessToken,
            'refresh_token': self.refreshToken,
            'role': self.role.value,
            'access_level': self.accesslevel.value,
            'cpf_rne': self.cpfRne,
            'email': self.email
        }
