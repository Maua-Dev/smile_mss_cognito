from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, IncompleteUser, InvalidCredentials
from src.domain.repositories.user_repository_interface import IUserRepository


class LoginUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, cpfRne: int, password: str) -> (str, str):
        tokens = await self._userRepository.loginUser(cpfRne, password)
        if tokens is None:
            raise InvalidCredentials(f'Cpf and password don`t match')

        accessToken, refreshToken = tokens
        if accessToken is None or refreshToken is None:
            raise InvalidCredentials(f'Cpf and password don`t match')
        return accessToken, refreshToken
