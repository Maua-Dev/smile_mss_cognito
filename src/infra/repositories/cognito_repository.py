from typing import List

import boto3 as boto3

from src.domain.entities.user import User
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infra.dtos.User.user_dto import CognitoUserDTO


class UserRepositoryCognito(IUserRepository):
    def __init__(self):
        self._client = boto3.client("cognito-idp", region_name="us-east-1")
        self._clientId = "5e8nadng13q2cnt5l93tk7fcki"
        self._userPoolId = "us-east-1_ppAG4yuxk"


    async def getUserByCpfRne(self, cpfRne: int) -> User:
        pass

    async def getAllUsers(self) -> List[User]:
        response = self._client.list_users(
            UserPoolId=self._userPoolId
        )
        users = []
        for user in response["Users"]:
            cognitoUserDTO = CognitoUserDTO.fromKeyValuePair(data=user["Attributes"])
            users.append(cognitoUserDTO.toEntity())
        return users, len(response["Users"])



    async def checkUserByPropriety(self, propriety: str, value: str) -> bool:
        pass

    async def createUser(self, user: CognitoUserDTO):
        return self._client.sign_up(
            ClientId=self._clientId,
            Username=user.name,
            Password=user.password,
            UserAttributes=user.userAttributes,
        )


    async def confirmUserCreation(self, user: CognitoUserDTO, code: str):
        return self._client.confirm_sign_up(
            ClientId=self._clientId,
            Username=user.name,
            ConfirmationCode=code
        )


    async def updateUser(self, user: User):
        pass

    async def deleteUser(self, userCpfRne: int):
        pass
