from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL


class CheckTokenViewmodel():
    role: ROLE
    access_level: ACCESS_LEVEL
    email: str
    user_id: str
    valid_token: bool

    def __init__(self, role: ROLE, access_level: ACCESS_LEVEL, email: str, valid_token: bool, user_id: str = None):
        self.role = role
        self.access_level = access_level
        self.email = email
        self.valid_token = valid_token
        self.user_id = user_id

    @staticmethod
    def from_dict(data: dict):
        return CheckTokenViewmodel(
            role=data['role'],
            access_level=data['access_level'],
            email=data['email'],
            valid_token=data['valid_token'],
            user_id=data['user_id']
        )

    def to_dict(self):
        return {
            'role': self.role,
            'access_level': self.access_level,
            'email': self.email,
            'valid_token': self.valid_token,
            'user_id': self.user_id if self.user_id else None
        }
