from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class LoginUserModel():
    accessToken: str
    refreshToken: str
    id: str
    role: ROLE
    accessLevel: ACCESS_LEVEL
    cpfRne: int
    email: str
    name: str
    socialName: str
    certificateWithSocialName: str

    def __init__(self, certificateWithSocialName: str, accessToken: str, refreshToken: str, role: str, accesslevel: str, cpfRne: int, email: str, socialName: str=None, name: str=None, id: str=None):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.role = role
        self.accessLevel = accesslevel
        self.certificateWithSocialName = certificateWithSocialName
        self.cpfRne = cpfRne
        self.email = email
        self.socialName = socialName
        self.name = name
        self.id = id

    @staticmethod
    def fromDict(data: dict):
        return LoginUserModel(
        accessToken = data['accessToken'],
        refreshToken = data['refreshToken'],
        role = data['role'],
        accesslevel = data['accessLevel'],
        cpfRne = data['cpfRne'],
        email = data['email'],
        socialName = data.get('socialName'),
        name = data.get('name'),
        certificateWithSocialName = data.get('certificateWithSocialName'),
        id = data.get('id')
        )

    def toDict(self):
        return {
            'access_token': self.accessToken,
            'refresh_token': self.refreshToken,
            'role': self.role.value,
            'access_level': self.accessLevel.value,
            'cpf_rne': self.cpfRne,
            'email': self.email,
            'social_name': self.socialName,
            'name': self.name,
            'certificate_with_social_name': self.certificateWithSocialName,
            'id': self.id
        }
