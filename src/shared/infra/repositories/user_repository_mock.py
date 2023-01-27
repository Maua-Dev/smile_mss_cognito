from typing import List, Tuple

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.domain.errors.errors import UnexpectedError, InvalidToken, UserAlreadyExists, InvalidCode, NonExistentUser, \
    UserAlreadyConfirmed
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class UserRepositoryMock(IUserRepository):

    users: List[User]
    confirmedUsers: List[User]

    def __init__(self):
        self.users = [
            User(user_id='0001', email='zeeba@gmail.com', name='Caio soller', password='z12345',
                 ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=1644977700000,
                 updated_at=1644977700000, social_name='zeeba toledo', accepted_terms=True,
                 accepted_notifications=True, certificate_with_social_name=True
                 ),
            User(user_id='0002', email='vitor@maua.br', name='vitor branco', password='z12345',
                 ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.ADMIN, created_at=1644977700000,
                 updated_at=1644977700000, social_name='zeeba toledo', accepted_terms=True,
                 accepted_notifications=True, certificate_with_social_name=True
                 ),
            User(user_id='0003', email='joao@gmail.com', name='João toledo', password='z12345',
                         ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=1644977700000,
                         updated_at=1644977700000, social_name='zeeba toledo', accepted_terms=True,
                         accepted_notifications=True, certificate_with_social_name=True
                 )
        ]
        self.confirmedUsers = [
            self.users[0],
            self.users[1]
        ]

    def get_all_users(self) -> List[User]:
        if len(self.confirmedUsers) > 0:
            return self.confirmedUsers
        else:
            return None

    def get_user_by_email(self, email: str) -> User:
        user: User = None
        for userx in self.confirmedUsers:
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

    def create_user(self, user: User):
        duplicitySensitive = ['user_id', 'email', 'ra']
        for field in duplicitySensitive:
            if self.check_user_by_propriety(propriety=field, value=getattr(user, field)):
                raise UserAlreadyExists(
                    f'Propriety ${field} = "${getattr(user, field)}" already exists')
        self.users.append(user)

    def confirm_user_creation(self, login: str, code: int) -> bool:
        # code = 1234567

        if code != 1234567:
            raise InvalidCode(f'Invalid code')
        user: User = None
        for userx in self.users:
            if userx.email == login:
                user = userx
                break
        if not user:
            raise NonExistentUser(f'User not found')
        if userx in self.confirmedUsers:
            raise UserAlreadyConfirmed(f'User already confirmed')
        self.confirmedUsers.append(user)
        return True

    def update_user(self, user: User) -> User:

        for idx, userx in enumerate(self.confirmedUsers):
            if userx.email == user.email:
                self.confirmedUsers[idx] = user
                return user

    def delete_user(self, email: str):
        cont = 0
        for userx in self.confirmedUsers:
            if userx.email == email:
                self.confirmedUsers.pop(cont)
                break
            cont += 1

    def login_user(self, email: str, password: str) -> dict:
        u = self.get_user_by_email(email)
        if u is None:
            return None
        if u.password == password:
            dictResponse = u.dict()
            dictResponse.pop('password')
            dictResponse["accessToken"] = "valid_access_token-" + str(email)
            dictResponse["refresh_token"] = "valid_refresh_token-" + str(email)
            return dictResponse
        return None

    def check_token(self, token: str) -> dict:

        split_token = token.split("-")
        if len(split_token) != 2 or split_token[0] != "validAccessToken":
            raise EntityError('token')

        email = split_token[1]
        user = self.get_user_by_email(email)

        if user is None:
            return None
        data = user.dict()
        data.pop('password')
        return data

    def refresh_token(self, refresh_token: str) -> Tuple[str, str]:
        splitToken = refresh_token.split("-")  # token, email
        if len(splitToken) != 2:
            return None, None
        if splitToken[0] != "valid_refresh_token":
            return None, None
        if self.get_user_by_email(splitToken[1]) is None:
            return None, None
        a = "valid_access_token-" + splitToken[1], refresh_token
        return a

    def change_password(self, login: str) -> bool:
        for userx in self.confirmedUsers:
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
            raise NonExistentUser(f"{email}")

        # Send email

        return True
