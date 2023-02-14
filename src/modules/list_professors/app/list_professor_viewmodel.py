from typing import List

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User


class UserViewmodel:
    name: str
    email: str
    ra: str
    role: ROLE
    access_level: ACCESS_LEVEL
    social_name: str
    phone: str

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.ra = user.ra
        self.role = user.role
        self.access_level = user.access_level
        self.social_name = user.social_name
        self.phone = user.phone

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'ra': self.ra,
            'role': self.role.value,
            'access_level': self.access_level.value,
            'social_name': self.social_name,
            'phone': self.phone,
        }


class ListProfessorsViewmodel:
    professors: List[UserViewmodel]

    def __init__(self, professors: List[User]):
        self.professors = [UserViewmodel(professor) for professor in professors]

    def to_dict(self):
        return {
            'professors': [professor.to_dict() for professor in self.professors],
            'message': 'the professors were retrieved'
        }
