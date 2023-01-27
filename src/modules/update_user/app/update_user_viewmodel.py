from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User


class UserViewmodel:
    name: str
    email: str
    ra: str
    role: ROLE
    access_level: ACCESS_LEVEL
    social_name: str
    accepted_notifications: bool
    certificate_with_social_name: bool

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.ra = user.ra
        self.role = user.role
        self.access_level = user.access_level
        self.social_name = user.social_name
        self.accepted_notifications = user.accepted_notifications
        self.certificate_with_social_name = user.certificate_with_social_name

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'ra': self.ra,
            'role': self.role.value,
            'access_level': self.access_level.value,
            'social_name': self.social_name,
            "accepted_notifications": self.accepted_notifications,
            "certificate_with_social_name": self.certificate_with_social_name
        }


class UpdateUserViewmodel:
    user: UserViewmodel

    def __init__(self, user: User):
        self.user = UserViewmodel(user)

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'message': 'the user was updated'
        }
