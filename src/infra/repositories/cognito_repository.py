from typing import List

import boto3 as boto3

from src.domain.entities.user import User
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infra.dtos.User.user_dto import CognitoUserDTO


class UserRepositoryCognito(IUserRepository):
    def __init__(self):
        self._client = boto3.client("cognito-idp", region_name="us-east-1")
        self._clientId = "5e8nadng13q2cnt5l93tk7fcki"


    async def getUserByCpfRne(self, cpfRne: int) -> User:
        pass

    def getAllUsers(self) -> List[User]:
        pass

    async def checkUserByPropriety(self, propriety: str, value: str) -> bool:
        pass

    async def createUser(self, user: CognitoUserDTO):

        response = self._client.sign_up(
            ClientId=self._clientId,
            Username=user.name,
            Password=user.password,
            UserAttributes=user.userAttributes,
        )
        return response


    async def confirmUserCreation(self, user: CognitoUserDTO, code: str):

        response = self._client.confirm_sign_up(
            ClientId=self._clientId,
            Username=user.name,
            ConfirmationCode=code
        )

        return response

    async def updateUser(self, user: User):
        pass

    async def deleteUser(self, userCpfRne: int):
        pass
