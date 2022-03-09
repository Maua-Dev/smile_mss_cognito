from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError
from src.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, user: User):
        try:

            duplicitySensitive = ['cpfRne', 'email', 'ra']
            for field in duplicitySensitive:
                if await self._userRepository.checkUserByPropriety(propriety=field, value=getattr(user, field)):
                    raise UserAlreadyExists(f'Propriety ${field} = "${getattr(user, field)}" already exists')

            await self._userRepository.createUser(user)

        except Exception as error:
            raise UnexpectedError('CreateUser', str(error))

