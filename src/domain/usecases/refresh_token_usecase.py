from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, IncompleteUser, InvalidCredentials, \
    InvalidToken
from src.domain.repositories.user_repository_interface import IUserRepository


class RefreshTokenUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, refreshToken: str) -> (str, str):
        tokens = await self._userRepository.refreshToken(refreshToken)
        if tokens is None or tokens == (None, None):
            raise InvalidToken(f'Invalid Refresh Token: {refreshToken}')

        accessToken, refreshToken = tokens
        if accessToken is None or refreshToken is None:
            raise InvalidToken(f'Invalid Refresh or Access Token')
        return accessToken, refreshToken
