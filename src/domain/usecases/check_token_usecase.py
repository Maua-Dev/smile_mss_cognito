from src.domain.errors.errors import InvalidToken
from src.domain.repositories.user_repository_interface import IUserRepository


class CheckTokenUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, cpfRne: int, token: str) -> bool:

        validatedToken = await self._userRepository.checkToken(cpfRne, token)

        if not validatedToken:
            raise InvalidToken('Invalid Token')

        return True

