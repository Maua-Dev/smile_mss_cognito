from typing import List

import boto3 as boto3

from src.domain.entities.user import User
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infra.dtos.User.user_dto import CognitoUserDTO


class UserRepositoryCognito(IUserRepository):

    def __init__(self):
        self._client = boto3.client("cognito-idp", region_name="us-east-1")
        self._clientId = "r5vor1epl6fclrfhovtlgiujh"
        self._userPoolId = "us-east-1_o2K6XlMyg"


    async def getUserByCpfRne(self, cpfRne: int) -> User:
        response = self._client.admin_get_user(
            UserPoolId=self._userPoolId,
            Username=str(cpfRne)
        )
        return CognitoUserDTO.fromKeyValuePair(data=response["UserAttributes"]).toEntity()

    async def getAllUsers(self) -> List[User]:
        response = self._client.list_users(
            UserPoolId=self._userPoolId
        )
        users = []
        for user in response["Users"]:
            cognitoUserDTO = CognitoUserDTO.fromKeyValuePair(data=user["Attributes"])
            users.append(cognitoUserDTO.toEntity())
        return users, len(response["Users"])


    async def createUser(self, user: User):
        user_dto = CognitoUserDTO(user.dict())

        self._client.sign_up(
            ClientId=self._clientId,
            Username=str(user_dto.cpfRne),
            Password=user_dto.password,
            UserAttributes=user_dto.userAttributes,
        )
        await self.confirmUserCreationAdmin(user_dto.cpfRne)


    async def confirmUserCreationAdmin(self, cpfRne: int):
        return self._client.admin_confirm_sign_up(
            UserPoolId=self._userPoolId,
            Username=str(cpfRne),

        )

    async def confirmUserCreation(self, user: CognitoUserDTO, code: str):
        return self._client.confirm_sign_up(
            ClientId=self._clientId,
            Username=str(user.cpfRne),
            ConfirmationCode=code
        )

    async def loginUser(self, cpfRne: int, password: str):
        response = self._client.initiate_auth(
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
