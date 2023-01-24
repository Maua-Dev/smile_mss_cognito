from src.domain.entities.user import User
from src.domain.errors.errors import UserAlreadyExists, UnexpectedError, NoItemsFound, NonExistentUser
from src.domain.repositories.user_repository_interface import IUserRepository
from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
from src.modules.get_user.app.get_user_usecase import GetUserByCpfRneUsecase


class UpdateUserUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository
        # self.immutable_fields = ['cpfRne', 'ra', 'acceptedTerms', 'accessLevel', 'email']
        self.mutatable_fields = [
            'name', 'socialName', 'acceptedNotifications', 'certificateWithSocialName']

    async def __call__(self, userData: dict, accessToken: str):
        checkTokenUsecase = CheckTokenUsecase(self._userRepository)
        try:
            oldUser = User.parse_obj(await checkTokenUsecase(accessToken))

            for field in self.mutatable_fields:
                if field in userData:
                    setattr(oldUser, field, userData[field])

            await self._userRepository.updateUser(oldUser)

        except NonExistentUser as error:
            raise NonExistentUser(error.message)
