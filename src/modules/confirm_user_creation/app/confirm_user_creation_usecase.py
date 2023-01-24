
from src.domain.repositories.user_repository_interface import IUserRepository


class ConfirmUserCreationUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, login: str, code: str) -> bool:
        result = await self._userRepository.confirmUserCreation(login, code)
        return result

