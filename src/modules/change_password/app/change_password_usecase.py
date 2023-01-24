from src.domain.errors.errors import InvalidToken
from src.domain.repositories.user_repository_interface import IUserRepository


class ChangePasswordUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, login: str) -> bool:

        data = await self._userRepository.changePassword(login)

        if not data:
            pass

        return data

