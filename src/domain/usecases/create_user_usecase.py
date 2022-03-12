from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, IncompleteUser
from src.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, user: User) -> int:
        try:

            requiredFields = ['name', 'cpfRne', 'email', 'password']
            for f in requiredFields:
                if getattr(user, f) is None:
                    raise IncompleteUser(f'field "{f}" is required')


            return await self._userRepository.createUser(user)


        except Exception as error:
            raise UnexpectedError('CreateUser', str(error))

