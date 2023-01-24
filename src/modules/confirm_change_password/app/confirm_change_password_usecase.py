from src.shared.domain.errors.errors import InvalidToken
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class ConfirmChangePasswordUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, login: str, newPassword: str, code: str) -> bool:

        result = await self._userRepository.confirmChangePassword(login, newPassword, code)

        if not result:
            pass

        return result
