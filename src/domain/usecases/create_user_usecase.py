from src.domain.entities.enums import ACCESS_LEVEL
from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, IncompleteUser, EntityError
from src.domain.repositories.user_repository_interface import IUserRepository


class CreateUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository

    async def __call__(self, user: User) -> int:
        requiredFields = ['name', 'cpfRne', 'email', 'password', 'acceptedNotifications', 'acceptedTerms']
        for f in requiredFields:
            if getattr(user, f) is None:
                raise IncompleteUser(f'field "{f}" is required')

        if user.accessLevel != ACCESS_LEVEL.USER:
            raise EntityError('Cannot create a user with ACCESS LEVEL different than USER')

        # Set default certificateWithSocialName based if user have social name
        user.certificateWithSocialName = True if user.socialName else False
        user.socialName = user.socialName if user.socialName else ""

        return await self._userRepository.createUser(user)
