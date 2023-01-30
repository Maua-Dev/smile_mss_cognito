from typing import Optional


class RefreshTokenViewmodel:
    accessToken: Optional[str]
    refreshToken: Optional[str]

    def __init__(self, access_token: Optional[str], refresh_token: Optional[str]):
        self.accessToken = access_token
        self.refreshToken = refresh_token

    def to_dict(self):
        return {
            'access_token': self.accessToken,
            'refresh_token': self.refreshToken,
            'message': "Token refreshed successfully"
        }
