from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class LoginUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, cpfRne: int, password: str) -> dict:
        loginResponseFields = ['cpfRne', 'accessToken',
                               'refreshToken', 'email', 'role', 'accessLevel']
        data = await self._userRepository.loginUser(cpfRne, password)
        if data is None:
            raise ForbiddenAction(f'Cpf and password don`t match')
        if not set(loginResponseFields) <= set(data.keys()):
            raise ForbiddenAction(
                f'Unexpected response from repository - missing fields from {loginResponseFields}')
        return data
