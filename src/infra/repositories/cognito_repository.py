import os
from typing import List

import boto3 as boto3
from botocore.exceptions import ClientError

from src.domain.entities.user import User
from src.domain.errors.errors import InvalidCredentials, NonExistentUser, BaseError, UserAlreadyExists, InvalidToken, \
    EntityError
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infra.dtos.User.user_dto import CognitoUserDTO


class UserRepositoryCognito(IUserRepository):


    def __init__(self):
        region = os.environ.get("AWS_REGION_COGNITO")
        userPoolId = os.environ.get("USER_POOL_ID")
        clientId = os.environ.get("CLIENT_ID")

        self._client = boto3.client("cognito-idp", region_name=region)
        self._clientId = clientId
        self._userPoolId = userPoolId


    async def getUserByCpfRne(self, cpfRne: int) -> User:
        try:
            response = self._client.admin_get_user(
                UserPoolId=self._userPoolId,
                Username=str(cpfRne)
            )
            return CognitoUserDTO.fromKeyValuePair(data=response["UserAttributes"]).toEntity()
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidCredentials("You don`t have permission to access this resource")
            elif errorCode == 'UserNotFoundException':
                raise NonExistentUser(f"{cpfRne}")
            else:
                raise

    async def getAllUsers(self) -> List[User]:
        try:
            response = self._client.list_users(
                UserPoolId=self._userPoolId
            )
            users = []
            for user in response["Users"]:
                cognitoUserDTO = CognitoUserDTO.fromKeyValuePair(data=user["Attributes"])
                users.append(cognitoUserDTO.toEntity())
            return users, len(response["Users"])
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidCredentials("You don`t have permission to access this resource")
            else:
                raise

    async def _checkIfUserExists(self, user) -> str:

        emailUsers = self._client.list_users(
            UserPoolId=self._userPoolId,
            Filter=f"email = \"{user.email}\""
        )
        if len(emailUsers["Users"]) > 0:
            return "email"


        if user.ra:
            raUsers = self._client.list_users(
                UserPoolId=self._userPoolId,
                Filter=f"preferred_username = \"{user.ra}\""
            )
            if len(raUsers["Users"]) > 0:
                return "ra"

        return None






    async def createUser(self, user: User):
        try:
            user_dto = CognitoUserDTO(user.dict())

            userAlreadyExist = await self._checkIfUserExists(user)
            if userAlreadyExist:
                raise UserAlreadyExists(f"{userAlreadyExist}")

            self._client.sign_up(
                ClientId=self._clientId,
                Username=str(user_dto.cpfRne),
                Password=user_dto.password,
                UserAttributes=user_dto.userAttributes,
            )
            await self._confirmUserCreationAdmin(user_dto.cpfRne, user_dto.ra)

        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidCredentials("You don`t have permission to access this resource")
            elif errorCode == 'InvalidParameterException':
                raise EntityError("Invalid parameter")
            elif errorCode == 'AliasExistsException':
                raise UserAlreadyExists("Alias already exists")
            elif errorCode == 'UsernameExistsException':
                raise UserAlreadyExists(f"{user.cpfRne}")
            elif errorCode == 'UserNotFoundException':
                raise NonExistentUser(f"{user.cpfRne}")
            else:
                raise BaseError(message=e.response.get('Error').get('Message'))





    async def _confirmUserCreationAdmin(self, cpfRne: str, ra:str):
        self._client.admin_confirm_sign_up(
            UserPoolId=self._userPoolId,
            Username=str(cpfRne),

        )
        self._client.admin_update_user_attributes(
            UserPoolId=self._userPoolId,
            Username=str(cpfRne),
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
                {
                    'Name': 'preferred_username',
                    'Value': str(ra)
                }
            ])


    async def confirmUserCreation(self, user: CognitoUserDTO, code: str):
        try:
            return self._client.confirm_sign_up(
                ClientId=self._clientId,
                Username=str(user.cpfRne),
                ConfirmationCode=code
            )
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidCredentials("You don`t have permission to access this resource")
            elif errorCode == 'InvalidParameterException':
                raise BaseError("Invalid parameter")
            elif errorCode == 'CodeMismatchException':
                raise InvalidCredentials("Invalid confirmation code")
            elif errorCode == 'ExpiredCodeException':
                raise InvalidCredentials("Expired confirmation code")
            raise BaseError(message=e.response.get('Error').get('Message'))

    async def loginUser(self, cpfRne: int, password: str) -> dict:
        try:
            responseLogin = self._client.initiate_auth(
                ClientId=self._clientId,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': str(cpfRne),
                    'PASSWORD': password
                }
            )
            responseGetUser = self._client.get_user(
                AccessToken=responseLogin["AuthenticationResult"]["AccessToken"]
            )

            user = CognitoUserDTO.fromKeyValuePair(data=responseGetUser["UserAttributes"]).toEntity()

            dictResponse = user.dict()
            dictResponse["accessToken"] = responseLogin["AuthenticationResult"]["AccessToken"]
            dictResponse["refreshToken"] = responseLogin["AuthenticationResult"]["RefreshToken"]
            return dictResponse

        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidCredentials(message="User or password invalid")
            elif errorCode == 'UserNotFoundException':
                raise NonExistentUser(message=f"{cpfRne}")
            elif errorCode == 'UserNotConfirmedException':
                raise InvalidCredentials(message="User not confirmed")
            else:
                raise BaseError(message=e.response.get('Error').get('Message'))



    async def checkToken(self, accessToken: str):
        try:
            response = self._client.get_user(
                AccessToken=accessToken
            )
            return CognitoUserDTO.fromKeyValuePair(data=response["UserAttributes"]).toEntity().dict()
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidToken(message="Invalid or expired Token")
            else:
                raise BaseError(message=e.response.get('Error').get('Message'))

    async def refreshToken(self, refreshToken: str) -> (str, str):
        try:
            response = self._client.initiate_auth(
                ClientId=self._clientId,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refreshToken
                }
            )
            return response["AuthenticationResult"]['AccessToken'], refreshToken
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidToken(message="Invalid or expired Token")
            else:
                raise BaseError(message=e.response.get('Error').get('Message'))

    async def changePassword(self, login: str) -> bool:
        try:
            response = self._client.forgot_password(
                ClientId=self._clientId,
                Username=login
            )
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'UserNotFoundException':
                raise NonExistentUser(message=f"{login}")
            elif errorCode == 'UserNotConfirmedException':
                raise BaseError(message="User not confirmed")
            else:
                raise BaseError(message=e.response.get('Error').get('Message'))


    async def confirmChangePassword(self, login: str, newPassword: str, code: str) -> bool:
        try:
            response = self._client.confirm_forgot_password(
                ClientId=self._clientId,
                Username=login,
                Password=newPassword,
                ConfirmationCode=code
            )
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'CodeMismatchException':
                raise InvalidCredentials(message="Invalid confirmation code")
            elif errorCode == 'UserNotFoundException':
                raise NonExistentUser(message=f"{login}")
            else:
                raise BaseError(message=e.response.get('Error').get('Message'))


    async def updateUser(self, user: User):
        pass

    async def deleteUser(self, userCpfRne: int):
        pass

