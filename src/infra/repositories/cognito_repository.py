from typing import List

import boto3 as boto3

from src.domain.entities.user import User
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infra.dtos.User.user_dto import CognitoUserDTO


class UserRepositoryCognito(IUserRepository):

    def __init__(self):
        self._client = boto3.client("cognito-idp", region_name="us-east-1")
        self._clientId = "oj4658u0c8uu5m186r68geitv"
        self._userPoolId = "us-east-1_zYP24SO9E"


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

    async def createUser(self, user: User):
        user_dto = CognitoUserDTO(user.dict())

        return self._client.sign_up(
            ClientId=self._clientId,
            Username=str(user_dto.cpfRne),
            Password=user_dto.password,
            UserAttributes=user_dto.userAttributes,
        )

    async def confirmUserCreation(self, user: CognitoUserDTO, code: str):
        return self._client.confirm_sign_up(
            ClientId=self._clientId,
            Username=str(user.cpfRne),
            ConfirmationCode=code
        )

    async def loginUser(self, cpfRne: int, password: str):
        response = await self._client.initiate_auth(
            ClientId=self._clientId,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': str(cpfRne),
                'PASSWORD': password
            }
        )
        return response["AuthenticationResult"]['AccessToken']

    async def checkToken(self, cpfRne: int, token: str):
        response = self._client.get_user(
            AccessToken=token
        )

        for attr in response['UserAttributes']:
            if attr['Name'] == 'custom:cpfRne' and attr['Value'] == str(cpfRne):
                return True
        return False

    async def updateUser(self, user: User):
        pass

    async def deleteUser(self, userCpfRne: int):
        pass
