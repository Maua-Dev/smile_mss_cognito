from src.domain.errors.errors import UnexpectedError, NoItemsFound
from src.domain.repositories.user_repository_interface import IUserRepository


class GetAllUsersUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self):
        try:
            users, count = await self._userRepository.getAllUsers()

            if users is None:
                raise NoItemsFound('')

            return users, count

        except NoItemsFound:
            raise NoItemsFound('GetAllUsers')


