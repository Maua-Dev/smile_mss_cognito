from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, NoItemsFound, NonExistentUser
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase


class UpdateUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository
        self.immutable_fields = ['cpfRne', 'ra']

    async def __call__(self, user: User): #TODO don`t update Null values
        try:
            # Check if immutable fields are changed
            getUserByCpfRneUsecase = GetUserByCpfRneUsecase(self._userRepository)
            oldUser = await getUserByCpfRneUsecase(user.cpfRne)
            for field in self.immutable_fields:
                if getattr(oldUser, field) != getattr(user, field):
                    raise UnexpectedError(f'{field} is immutable')

            await self._userRepository.updateUser(user)

        except (NonExistentUser) as error:
            raise NonExistentUser(error.message)

        except Exception as error:
            raise UnexpectedError('UpdateUser', str(error))

