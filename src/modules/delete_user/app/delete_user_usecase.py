from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, NoItemsFound, NonExistentUser
from src.domain.repositories.user_repository_interface import IUserRepository
from src.modules.get_user.app.get_user_usecase import GetUserByCpfRneUsecase


class DeleteUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, cpfRne: int):
        try:
            # Check if immutable fields are changed
            getUserByCpfRneUsecase = GetUserByCpfRneUsecase(
                self._userRepository)
            await getUserByCpfRneUsecase(cpfRne)

            await self._userRepository.deleteUser(cpfRne)

        except (NoItemsFound, NonExistentUser) as error:
            raise NonExistentUser(error.message)
