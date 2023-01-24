from src.shared.domain.errors.errors import InvalidToken
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class CheckTokenUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def __call__(self, token: str) -> dict:

        data = await self.repo.checkToken(token)

        if not data:
            raise InvalidToken('Invalid Token')

        return data
