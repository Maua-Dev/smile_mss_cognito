from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError, NoItemsFound, NonExistentUser
from src.domain.repositories.user_repository_interface import IUserRepository


class GetUserByCpfRneUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, cpf_rne: int) -> User:
        try:
            user = await self._userRepository.getUserByCpfRne(cpfRne=int(cpf_rne))

            if user is None:
                raise NonExistentUser('')

            return user

        except (NoItemsFound, NonExistentUser) as error:
            raise NonExistentUser(str(error))

        except Exception as error:
            raise UnexpectedError('GetUserByCpfRne', str(error))


