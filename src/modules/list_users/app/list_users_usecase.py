from src.domain.entities.enums import ACCESS_LEVEL
from src.domain.entities.user import User
from src.domain.errors.errors import NonExistentUser, InvalidCredentials
from src.domain.repositories.user_repository_interface import IUserRepository
from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase


class ListUsersUsecase:

    def __init__(self, userRepository: IUserRepository):
        self._userRepository = userRepository
        # self.immutable_fields = ['cpfRne', 'ra', 'acceptedTerms', 'accessLevel', 'email']
        self.mutatable_fields = [
            'name', 'socialName', 'acceptedNotifications', 'certificateWithSocialName']

    async def __call__(self, userList: list, accessToken: str):
        checkTokenUsecase = CheckTokenUsecase(self._userRepository)
        try:
            userRequester = User.parse_obj(await checkTokenUsecase(accessToken))
            if userRequester.accessLevel != ACCESS_LEVEL.ADMIN:
                raise InvalidCredentials(f"{userRequester.email} not admin")

            allUsers = await self._userRepository.getAllUsers()
            userDict = {}
            for user in allUsers:
                if user.id in userList:
                    userDict[user.id] = user.dict()

            if len(userDict) != len(userList):
                for id in userList:
                    if id not in userDict.keys():
                        userDict[id] = {"error": f"User not found"}

            return userDict

        except NonExistentUser as error:
            raise NonExistentUser(error.message)
