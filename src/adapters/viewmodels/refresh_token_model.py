from typing import Optional


class RefreshTokenModel():
    accessToken: Optional[str]
    refreshToken: Optional[str]

    def __init__(self, accessToken: Optional[str], refreshToken: Optional[str]):
        self.accessToken = accessToken
        self.refreshToken = refreshToken

    def toDict(self):
        return {
            'access_token': self.accessToken,
            'refresh_token': self.refreshToken
        }
