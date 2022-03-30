from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class LoginUserModel():
    accessToken: str
    refreshToken: str
    role: ROLE
    accesslevel: ACCESS_LEVEL
    cpfRne: int
    email: str
    socialName: str

    def __init__(self, accessToken: str, refreshToken: str, role: str, accesslevel: str, cpfRne: int, email: str, socialName: str=None):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.role = role
        self.accesslevel = accesslevel
        self.cpfRne = cpfRne
        self.email = email
        self.socialName = socialName

    @staticmethod
    def fromDict(data: dict):
        return LoginUserModel(
        accessToken = data['accessToken'],
        refreshToken = data['refreshToken'],
        role = data['role'],
        accesslevel = data['accessLevel'],
        cpfRne = data['cpfRne'],
        email = data['email'],
        socialName = data.get('socialName')
        )

    def toDict(self):
        return {
            'access_token': self.accessToken,
            'refresh_token': self.refreshToken,
            'role': self.role.value,
            'access_level': self.accesslevel.value,
            'cpf_rne': self.cpfRne,
            'email': self.email,
            'social_name': self.socialName
        }
