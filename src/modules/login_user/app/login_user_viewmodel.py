from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE


class UserViewmodel:
    access_token: str
    refresh_token: str
    ra: str
    user_id: str
    role: str
    access_level: str
    email: str
    name: str
    phone: str
    social_name: str
    certificate_with_social_name: str

    def __init__(self, certificate_with_social_name: str, access_token: str, refresh_token: str, role: str, access_level: str, email: str, phone: str, social_name: str = None, name: str = None, user_id: str = None, ra: str = None, **kwargs):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.ra = ra
        self.role = role
        self.access_level = access_level
        self.certificate_with_social_name = certificate_with_social_name
        self.email = email
        self.phone = phone
        self.social_name = social_name
        self.name = name
        self.user_id = user_id

    def to_dict(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'ra': self.ra,
            'role': self.role,
            'access_level': self.access_level,
            'email': self.email,
            'phone': self.phone,
            'social_name': self.social_name,
            'name': self.name,
            'certificate_with_social_name': self.certificate_with_social_name,
            'user_id': self.user_id,
        }


class LoginUserViewmodel:
    user: UserViewmodel

    def __init__(self, data: dict):
        self.user = UserViewmodel(**data)

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'message': 'Login successful'
        }
