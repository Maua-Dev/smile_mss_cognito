from typing import Optional

from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class CheckTokenModel:
    tokenValidated: bool
    role: ROLE
    accessLevel: ACCESS_LEVEL

    def __init__(self, tokenValidated: bool, role: ROLE, accessLevel: ACCESS_LEVEL):
        self.tokenValidated = tokenValidated
        self.role = role
        self.accessLevel = accessLevel

    @staticmethod
    def fromDict(obj: dict) -> 'CheckTokenModel':
        return CheckTokenModel(
            tokenValidated=obj['tokenValidated'],
            role=ROLE(obj['role']),
            accessLevel=ACCESS_LEVEL(obj['accessLevel'])
        )

    def toDict(self):
        return {
            'token_validated': self.tokenValidated,
            'role': self.role.value,
            'access_level': self.accessLevel.value
        }

