from typing import Tuple, List

import boto3

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
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

        all_users = [UserCognitoDTO.from_cognito(user).to_entity() for user in all_users]

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

    def update_user(self, user: User) -> User:
        pass

    def delete_user(self, cpfRne: int):
        pass

    def confirm_user_creation(self, login: str, code: int):
        pass

    def login_user(self, login: str, password: str) -> dict:
        pass

    def check_token(self, token: str) -> dict:
        pass

    def refresh_token(self, refreshToken: str) -> Tuple[str, str]:
        pass

    def change_password(self, login: str) -> bool:
        pass

    def confirm_change_password(self, login: str, newPassword: str, code: str) -> bool:
        pass

    def resend_confirmation_code(self, email: str) -> bool:
        pass
