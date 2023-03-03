from typing import List, Tuple

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, DuplicatedItem, UserNotConfirmed, \
    InvalidCredentials, UserAlreadyConfirmed


class UserRepositoryMock(IUserRepository):

    users: List[User]
    confirmed_users: List[User]

    def __init__(self):
        self.users = [
            User(user_id='000000000000000000000000000000000001', email='zeeba@gmail.com', name='Caio soller', password='z12345',
                 ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                 updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                 accepted_notifications_sms=True, certificate_with_social_name=True, phone="5511999451100", accepted_notifications_email=True
                 ),
            User(user_id='000000000000000000000000000000000002', email='vitor@maua.br', name='vitor branco', password='z12345',
                 ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.ADMIN, created_at=16449777000,
                 updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                 accepted_notifications_sms=True, certificate_with_social_name=False, phone="5511991758098", accepted_notifications_email=False
                 ),
            User(user_id='000000000000000000000000000000000003', email='joao@gmail.com', name='João toledo', password='z12345',
                         ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                         updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                         accepted_notifications_sms=True, certificate_with_social_name=True, phone="5511991758098", accepted_notifications_email=False
                 ),
            User(user_id='000000000000000000000000000000000004', email='professorvitor@gmail.com', name='Vitor toledo',
                 password='z12345',
                 ra=None, role=ROLE.PROFESSOR, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                 updated_at=16449777000, social_name=None, accepted_terms=True,
                 accepted_notifications_sms=True, certificate_with_social_name=False, phone="5511991758098", accepted_notifications_email=True
                 )
        ]
        self.confirmed_users = [
            self.users[0],
            self.users[1],
            self.users[3],
        ]

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
                    getattr(user, field))
        self.users.append(user)
        return user

    def confirm_user_creation(self, email: str, confirmation_code: str) -> bool:
        for u in self.confirmed_users:
            if u.email == email:
                raise UserAlreadyConfirmed("user")

        not_confirmed_user = True

        for u in self.users:
            if u.email == email:
                not_confirmed_user = False
                break

        if not_confirmed_user:
            raise NoItemsFound("user")

        # confirmation_code = '102030'
        if confirmation_code != '102030':
            raise InvalidCredentials('confirmation_code')

        user = self.get_user_by_email(email)
        self.confirmed_users.append(user)
        return True

    def update_user(self, user_email: str, kvp_to_update: dict) -> User:

        for idx, userx in enumerate(self.confirmed_users):
            if userx.email == user_email:
                for key, value in kvp_to_update.items():
                    setattr(userx, key, value)
                return userx

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
            dict_response["id_token"] = "valid_id_token-" + str(email)
            return dict_response
        return None

    def check_token(self, token: str) -> dict:

        split_token = token.split("-")
        if len(split_token) != 2 or split_token[0] != "valid_access_token":
            raise EntityError('access_token')

        email = split_token[1]
        user = self.get_user_by_email(email)

        if user is None:
            return None

        data = user.to_dict()
        data.pop('password')
        return data

    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        split_token = refresh_token.split("-")  # token, email
        if len(split_token) != 2:
            return None, None
        if split_token[0] != "valid_refresh_token":
            return None, None
        if self.get_user_by_email(split_token[1]) is None:
            return None, None
        tokens = "valid_access_token-" + split_token[1], refresh_token, "valid_id_token-" + split_token[1]
        return tokens

    def change_password(self, email: str) -> bool:
        for userx in self.confirmed_users:
            if userx.email == email:
                return True
        return False

    def confirm_change_password(self, email: str, new_password: str, confirmation_code: str) -> bool:
        # confirmation_code = 123456

        # Check code
        if confirmation_code != "123456":
            return False

        # Update user password
        user = self.get_user_by_email(email)
        if user:
            user.password = new_password
            return True
        return False

    def resend_confirmation_code(self, email: str) -> bool:
        user = self.get_user_by_email(email)

        if user is None:
            raise NoItemsFound(f"user email: {email}")

        # Send email in real repository

        return True

    def list_professors(self) -> List[User]:
        list_professor = list()

        for user in self.confirmed_users:
            if user.role == ROLE.PROFESSOR:
                list_professor.append(user)

        return list_professor
