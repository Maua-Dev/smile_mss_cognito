from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class ListUserError():
    def __init__(self, message):
        self.message = message

    def toDict(self):
        return self.message


class ListUserModel():
    role: ROLE
    accessLevel: ACCESS_LEVEL
    cpfRne: int
    email: str
    name: str
    socialName: str
    certificateWithSocialName: str

    def __init__(self, role: ROLE, accessLevel: ACCESS_LEVEL, cpfRne: int, email: str, name: str, socialName: str, certificateWithSocialName: str):
        self.role = role
        self.accessLevel = accessLevel
        self.cpfRne = cpfRne
        self.email = email
        self.name = name
        self.socialName = socialName
        self.certificateWithSocialName = certificateWithSocialName

    def fromDict(dict):
        if "error" in dict:
            return ListUserError(dict)
        return ListUserModel(
            role=dict.get('role').value if dict.get('role') else None,
            accessLevel=dict.get('accessLevel').value if dict.get('accessLevel') else None,
            cpfRne=dict.get('cpfRne') if dict.get('cpfRne') else None,
            email=dict.get('email') if dict.get('email') else None,
            name=dict.get('name') if dict.get('name') else None,
            socialName=dict.get('socialName') if dict.get('socialName') else None,
            certificateWithSocialName=dict.get('certificateWithSocialName') if dict.get('certificateWithSocialName') else None
        )

    def toDict(self):
        return {
            'role': self.role,
            'accessLevel': self.accessLevel,
            'cpfRne': self.cpfRne,
            'email': self.email,
            'name': self.name,
            'socialName': self.socialName,
            'certificateWithSocialName': self.certificateWithSocialName
        }

class ListUsersModel():
    users: dict

    def __init__(self, usersDict: dict):
        self.users = {}
        for userId in usersDict.keys():
            userModel = ListUserModel.fromDict(usersDict[userId])
            self.users[userId] = userModel.toDict()

    def toDict(self):
        return self.users



