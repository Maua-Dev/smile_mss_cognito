from typing import Tuple, List

import boto3
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.dtos.User.user_cognito_dto import UserCognitoDTO


class UserRepositoryCognito(IUserRepository):

    client: boto3.client
    user_pool_id: str
    client_id: str

    def __init__(self):
        self.client = boto3.client('cognito-idp')
        self.user_pool_id = Environments.get_envs().user_pool_id
        self.client_id = Environments.get_envs().client_id

    def get_user_by_email(self, email: str) -> User:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            if response["UserStatus"] == "UNCONFIRMED":
                return None

            user = UserCognitoDTO.from_cognito(response).to_entity()
            return user

        except self.client.exceptions.UserNotFoundException:
            return None

    def get_all_users(self) -> List[User]:
        kwargs = {
            'UserPoolId': self.user_pool_id
        }

        all_users = list()
        users_remain = True
        next_page = None

        while users_remain:
            if next_page:
                kwargs['PaginationToken'] = next_page
            response = self.client.list_users(**kwargs)


            all_users.extend(response["Users"])
            next_page = response.get('PaginationToken', None)
            users_remain = next_page is not None

        all_users = [UserCognitoDTO.from_cognito(user).to_entity() for user in all_users if user["UserStatus"] == "CONFIRMED"]

        return all_users

    def create_user(self, user: User) -> User:
        cognito_attributes = UserCognitoDTO.from_entity(user).to_cognito_attributes()

        response = self.client.sign_up(
            ClientId=self.client_id,
            Username=user.email,
            Password=user.password,
            UserAttributes=cognito_attributes)

        user.cognito_id = response.get("UserSub")

        return user

    def update_user(self, user_email: str, kvp_to_update: dict) -> User:
        response = self.client.admin_update_user_attributes(
            UserPoolId=self.user_pool_id,
            Username=user_email,
            UserAttributes=[{'Name': UserCognitoDTO.TO_COGNITO_DICT[key], 'Value': value} for key, value in kvp_to_update.items()]
        )

        return self.get_user_by_email(user_email)


    def delete_user(self, user_email: str):
        self.client.admin_delete_user(
            UserPoolId=self.user_pool_id,
            Username=user_email
        )

        return

    def confirm_user_creation(self, login: str, code: int):
        try:
            userResult = self.client.list_users(
                UserPoolId=self.user_pool_id,
                Filter=f'email = "{login}"'
            )
            # check erros
            userList = userResult["Users"]

            if len(userList) == 0:
                raise ForbiddenAction(f"{login}")

            if userList[0]["UserStatus"] == "CONFIRMED":
                raise ForbiddenAction(f"{login} is already confirmed")

            user = userList[0]
            userParsed = UserCognitoDTO.from_cognito(data=user)

            if not userParsed:
                raise ForbiddenAction(f"{login}")

            return self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=userParsed.email,
                ConfirmationCode=code
            )
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise ForbiddenAction("You don`t have permission to access this resource")
            elif errorCode == 'InvalidParameterException':
                raise ForbiddenAction(e.response.get('Error').get('Message'))
            elif errorCode == 'CodeMismatchException':
                raise ForbiddenAction("Invalid confirmation code")
            elif errorCode == 'ExpiredCodeException':
                raise ForbiddenAction("Expired confirmation code")
            raise ForbiddenAction(message=e.response.get('Error').get('Message'))

    def login_user(self, login: str, password: str) -> dict:
        try:
            responseLogin = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': str(login),
                    'PASSWORD': password
                }
            )
            responseGetUser = self.client.get_user(
                AccessToken=responseLogin["AuthenticationResult"]["AccessToken"]
            )

            user = UserCognitoDTO.from_cognito(responseGetUser).to_entity()

            dictResponse = user.to_dict()
            dictResponse["access_token"] = responseLogin["AuthenticationResult"]["AccessToken"]
            dictResponse["refresh_token"] = responseLogin["AuthenticationResult"]["RefreshToken"]
            dictResponse["id_token"] = responseLogin["AuthenticationResult"]["IdToken"]
            return dictResponse

        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise ForbiddenAction(message="User or password invalid")
            elif errorCode == 'UserNotFoundException':
                raise ForbiddenAction(message=f"{login}")
            elif errorCode == 'UserNotConfirmedException':
                raise ForbiddenAction(message=f"{login}")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))

    def check_token(self, token: str) -> dict:
        try:
            response = self.client.get_user(
                AccessToken=token
            )

            return UserCognitoDTO.from_cognito(response).to_entity().to_dict()
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise ForbiddenAction(message="Invalid or expired Token")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))

    def refresh_token(self, refresh_token: str) -> Tuple[str, str]:
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )
            return response["AuthenticationResult"]['AccessToken'], refresh_token
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise ForbiddenAction(message="Invalid or expired Token")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))

    def change_password(self, login: str) -> bool:
        try:
            userCognitoDTO = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=login
            )
            user = UserCognitoDTO.from_cognito(userCognitoDTO).to_entity()

            response = self.client.forgot_password(
                ClientId=self.client_id,
                Username=login,
                ClientMetadata={
                    'login': user.email
                }
            )
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'UserNotFoundException':
                raise ForbiddenAction(message=f"{login}")
            elif errorCode == 'UserNotConfirmedException':
                raise ForbiddenAction(message=f"{login}")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))

    def confirm_change_password(self, login: str, newPassword: str, code: str) -> bool:
        try:
            response = self.client.confirm_forgot_password(
                ClientId=self.client_id,
                Username=login,
                Password=newPassword,
                ConfirmationCode=code
            )
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'CodeMismatchException':
                raise ForbiddenAction(message="Invalid confirmation code")
            elif errorCode == 'UserNotFoundException':
                raise ForbiddenAction(message=f"{login}")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))

    def resend_confirmation_code(self, email: str) -> bool:
        try:
            response = self.client.resend_confirmation_code(
                ClientId=self.client_id,
                Username=email
            )
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'UserNotFoundException':
                raise ForbiddenAction(message=f"{email}")
            elif errorCode == 'InvalidParameterException':
                if e.response.get('Error').get('Message') == 'User is already confirmed.':
                    raise ForbiddenAction(message=f"{email}")
                else:
                    raise ForbiddenAction(e.response.get('Error').get('Message'))
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))
