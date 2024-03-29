from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User


class UserViewmodel:
    name: str
    email: str
    ra: str
    role: ROLE
    access_level: ACCESS_LEVEL
    social_name: str
    accepted_notifications_sms: bool
    certificate_with_social_name: bool
    phone: str

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.ra = user.ra
        self.role = user.role
        self.access_level = user.access_level
        self.social_name = user.social_name
        self.accepted_notifications_sms = user.accepted_notifications_sms
        self.accepted_notifications_email = user.accepted_notifications_email
        self.certificate_with_social_name = user.certificate_with_social_name
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
            "accepted_notifications_sms": self.accepted_notifications_sms,
            'accepted_notifications_email': self.accepted_notifications_email,
            "certificate_with_social_name": self.certificate_with_social_name,
            'phone': self.phone,
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
