from src.domain.entities.user import User
from src.domain.errors.errors import EntityError
from src.domain.repositories.user_repository_interface import IUserRepository


class ResendCreationConfirmationUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, cpfRne: str) -> bool:
        if not User.validateCpf(cpfRne):
            raise EntityError("CPF")

        result = await self._userRepository.resendConfirmationCode(cpfRne)
        return result

