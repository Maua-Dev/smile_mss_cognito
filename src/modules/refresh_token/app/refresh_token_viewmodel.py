from typing import Optional


class RefreshTokenViewmodel:
    access_token: Optional[str]
    refresh_token: Optional[str]
    id_token: Optional[str]

    def __init__(self, access_token: Optional[str], refresh_token: Optional[str], id_token: Optional[str]):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token

    def to_dict(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'id_token': self.id_token,
            'message': "Token refreshed successfully"
        }
