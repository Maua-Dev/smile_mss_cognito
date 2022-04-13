from pydantic.main import BaseModel
from datetime import datetime
from typing import Optional

from src.domain.entities.enums import ACCESS_LEVEL, ROLE


class DbBaseModel():
    name: str
    cpfRne: str
    password: Optional[str]
    ra: Optional[int]
    email: Optional[str]
    role: ROLE
    accessLevel: ACCESS_LEVEL
    acceptedTerms: Optional[bool]
    acceptedNotific: Optional[bool]
    certWithSocialName: Optional[bool]
    socialName: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


    def __init__(self, data: dict):
        self.name = data.get('name')
        self.cpfRne = data.get('cpfRne') if data.get('cpfRne') else None
        self.password = data.get('password')
        self.ra = int(data.get('ra')) if data.get('ra') else None
        self.email = data.get('email')
        self.role = data.get('role')
        self.accessLevel = data.get('accessLevel')
        self.socialName = data.get('socialName')
        self.acceptedTerms = eval(str(data.get('acceptedTerms'))) if 'acceptedTerms' in data else None
        self.acceptedNotific = eval(str(data.get('acceptedNotifications'))) if 'acceptedNotifications' in data else None
        self.certWithSocialName = eval(str(data.get('certificateWithSocialName'))) if 'certificateWithSocialName' in data else None
        # self.createdAt = data.get('createdAt')
        # self.updatedAt = data.get('updatedAt')

    def to_dict(self):
        return self.__dict__



