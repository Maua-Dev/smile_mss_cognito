from src.domain.errors.errors import InvalidToken
from src.domain.repositories.user_repository_interface import IUserRepository


class CheckTokenUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, token: str) -> dict:

        data = await self._userRepository.checkToken(token)

        if not data:
            raise InvalidToken('Invalid Token')
        data["tokenValidated"] = True

        return data

