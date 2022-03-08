from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError, NoItemsFound
from src.domain.repositories.user_repository_interface import IUserRepository


class GetUserByCpfRneUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    def __call__(self, cpf_rne: int) -> User:
        try:
            user = self._userRepository.getUserByCpfRne(cpfRne=cpf_rne)
            print(user)

            if user is None:
                raise NoItemsFound('')

            return user

        except NoItemsFound:
            raise NoItemsFound('GetUserByCpfRne')

        except Exception as error:
            raise UnexpectedError('GetUserByCpfRne', str(error))

