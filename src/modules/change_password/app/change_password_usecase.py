from src.shared.domain.errors.errors import InvalidToken
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class ChangePasswordUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def __call__(self, login: str) -> bool:

        data = await self.repo.changePassword(login)

        if not data:
            pass

        return data
