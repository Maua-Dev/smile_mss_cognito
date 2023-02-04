from typing import List, Tuple

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, DuplicatedItem


class UserRepositoryMock(IUserRepository):

    users: List[User]
    confirmed_users: List[User]

    def __init__(self):
        self.users = [
            User(user_id='000000000000000000000000000000000001', email='zeeba@gmail.com', name='Caio soller', password='z12345',
                 ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                 updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                 accepted_notifications=True, certificate_with_social_name=True, phone="5511999451100"
                 ),
            User(user_id='000000000000000000000000000000000002', email='vitor@maua.br', name='vitor branco', password='z12345',
                 ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.ADMIN, created_at=16449777000,
                 updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                 accepted_notifications=True, certificate_with_social_name=False, phone="5511991758098"
                 ),
            User(user_id='000000000000000000000000000000000003', email='joao@gmail.com', name='João toledo', password='z12345',
                         ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                         updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                         accepted_notifications=True, certificate_with_social_name=True, phone="5511991758098"
                 )
        ]
        self.confirmed_users = [
            self.users[0],
            self.users[1]
        ]

    def get_confirmed_users(self) -> List[User]:
        return self.confirmed_users

    def get_all_users(self) -> List[User]:
        if len(self.confirmed_users) > 0:
            return self.confirmed_users
        else:
            return None

    def get_user_by_email(self, email: str) -> User:
        user: User = None
        for userx in self.confirmed_users:
            if userx.email == email:
                user = userx
                break
            pass
        return user

    # Busca na lista que possui confirmados e não confirmados
    def get_unconfirmed_user_by_email(self, email: str) -> User:
        user: User = None
        for userx in self.users:
            if userx.email == email:
                user = userx
                break
            pass
        return user

    def check_user_by_propriety(self, propriety: str, value: str) -> bool:
        for userx in self.users:
            if getattr(userx, propriety) == value and value != None:
                return True
        return False

    def create_user(self, user: User) -> User:
        duplicity_sensitive = ['user_id', 'email', 'ra']
        user.user_id = '00000000000000000000000000000000000' + \
            str(len(self.users) + 1)
        for field in duplicity_sensitive:
            if self.check_user_by_propriety(propriety=field, value=getattr(user, field)):
                raise DuplicatedItem(
                    f'User: {field} = "{getattr(user, field)}"')
        self.users.append(user)
        return user

    def confirm_user_creation(self, email: str, confirmation_code: str) -> bool:
        pass
    #     # code = 1234567
    #
    #     if code != 1234567:
    #         raise InvalidCode(f'Invalid code')
    #     user: User = None
    #     for userx in self.users:
    #         if userx.email == login:
    #             user = userx
    #             break
    #     if not user:
    #         raise NonExistentUser(f'User not found')
    #     if userx in self.confirmed_users:
    #         raise UserAlreadyConfirmed(f'User already confirmed')
    #     self.confirmed_users.append(user)
    #     return True

        # confirmation_code = '102030'
        if confirmation_code != '102030':
            raise ForbiddenAction('"Invalid Confirmation Code".')

        user = self.get_user_by_email(email)
        self.confirmed_users.append(user)
        return True

    def update_user(self, user: User) -> User:

        for idx, userx in enumerate(self.confirmed_users):
            if userx.email == user.email:
                self.confirmed_users[idx] = user
                return user

        return None

    def delete_user(self, email: str):
        cont = 0
        for userx in self.confirmed_users:
            if userx.email == email:
                self.confirmed_users.pop(cont)
                break
            cont += 1

    def login_user(self, email: str, password: str) -> dict:
        user = self.get_user_by_email(email)
        if user is None:
            return None
        if user.password == password:
            dict_response = user.to_dict()
            dict_response.pop('password')
            dict_response["access_token"] = "valid_access_token-" + str(email)
            dict_response["refresh_token"] = "valid_refresh_token-" + \
                str(email)
            return dict_response
        return None

    def check_token(self, token: str) -> dict:

        split_token = token.split("-")
        if len(split_token) != 2 or split_token[0] != "valid_access_token":
            raise EntityError('token')

        email = split_token[1]
        user = self.get_user_by_email(email)

        if user is None:
            return None

        data = user.to_dict()
        data.pop('password')
        return data

    def refresh_token(self, refresh_token: str) -> Tuple[str, str]:
        split_token = refresh_token.split("-")  # token, email
        if len(split_token) != 2:
            return None, None
        if split_token[0] != "valid_refresh_token":
            return None, None
        if self.get_user_by_email(split_token[1]) is None:
            return None, None
        a = "valid_access_token-" + split_token[1], refresh_token
        return a

    def change_password(self, login: str) -> bool:
        for userx in self.confirmed_users:
            if userx.email == login:
                return True
        return False

    def confirm_change_password(self, login: str, newPassword: str, code: str) -> bool:
        # code = 123456

        # Check code
        if code != "123456":
            return False

        # Update user password
        user = self.get_user_by_email(login)
        if user:
            user.password = newPassword
            return True
        return False

    def resend_confirmation_code(self, email: str) -> bool:
        user = self.get_user_by_email(email)

        if user is None:
            raise NoItemsFound(f"user email: {email}")

        # Send email in real repository

        return True
