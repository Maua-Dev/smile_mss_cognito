from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, IncompleteUser
from src.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, user: User) -> int:
        try:

            duplicitySensitive = ['cpfRne', 'email', 'ra']
            requiredFields = ['name', 'cpfRne', 'email', 'password']
            for f in requiredFields:
                if getattr(user, f) is None:
                    raise IncompleteUser(f'field "{f}" is required')
            for field in duplicitySensitive: #TODO isso está ruim - implementar logica dentro do repo
                if await self._userRepository.checkUserByPropriety(propriety=field, value=getattr(user, field)):
                    raise UserAlreadyExists(f'Propriety ${field} = "${getattr(user, field)}" already exists')

            return await self._userRepository.createUser(user)


        except Exception as error:
            raise UnexpectedError('CreateUser', str(error))

