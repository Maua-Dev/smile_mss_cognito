from datetime import datetime
from typing import List, Tuple

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.domain.errors.errors import UnexpectedError, InvalidToken, UserAlreadyExists, InvalidCode, NonExistentUser, \
    UserAlreadyConfirmed
from src.shared.domain.repositories.user_repository_interface import IUserRepository


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
                 ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=1644977700000,
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
            self._users[0],
            self._users[1]
        ]

    def getAllUsers(self) -> List[User]:
        if len(self.confirmedUsers) > 0:
            return self.confirmedUsers
        else:
            return None

    def getUserByEmail(self, email: str) -> User:
        user: User = None
        for userx in self.confirmedUsers:
            if userx.email == email:
                user = userx
                break
            pass
        return user

    def checkUserByPropriety(self, propriety: str, value: str) -> bool:
        for userx in self._users:
            if getattr(userx, propriety) == value and value != None:
                return True
        return False

    def createUser(self, user: User):
        duplicitySensitive = ['user_id', 'email', 'ra']
        for field in duplicitySensitive:
            if self.checkUserByPropriety(propriety=field, value=getattr(user, field)):
                raise UserAlreadyExists(
                    f'Propriety ${field} = "${getattr(user, field)}" already exists')
        self._users.append(user)

    def confirmUserCreation(self, login: str, code: int) -> bool:
        # code = 1234567

        if code != "1234567":
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

    def updateUser(self, user: User):
        cont = 0
        for userx in self.confirmedUsers:
            if userx.email == user.email:
                break
            cont += 1

        self.confirmedUsers[cont] = user

    def deleteUser(self, email: str):
        cont = 0
        for userx in self.confirmedUsers:
            if userx.email == email:
                self.confirmedUsers.pop(cont)
                break
            cont += 1

    def loginUser(self, email: str, password: str) -> dict:
        u = self.getUserByEmail(email)
        if u is None:
            return None
        if u.password == password:
            dictResponse = u.dict()
            dictResponse.pop('password')
            dictResponse["accessToken"] = "validAccessToken-" + str(email)
            dictResponse["refreshToken"] = "validRefreshToken-" + str(email)
            return dictResponse
        return None

    def checkToken(self, token: str) -> dict:
        splitToken = token.split("-")
        if len(splitToken) != 2:
            return None
        if splitToken[0] != "validAccessToken":
            return None

        email = splitToken[1]
        user = self.getUserByEmail(email)
        if user is None:
            return None
        data = user.dict()
        data.pop('password')
        return data

    def refreshToken(self, refreshToken: str) -> Tuple[str, str]:
        splitToken = refreshToken.split("-")  # token, email
        if len(splitToken) != 2:
            return None, None
        if splitToken[0] != "validRefreshToken":
            return None, None
        if self.getUserByEmail(splitToken[1]) is None:
            return None, None
        return "validAccessToken-" + splitToken[1], refreshToken

    def changePassword(self, login: str) -> bool:
        user = None
        if login.isdigit():
            user = self.getUserByEmail(login)
        if user:
            return True

        for userx in self.confirmedUsers:
            if userx.email == login:
                return True
        return False

    def confirmChangePassword(self, login: str, newPassword: str, code: str) -> bool:
        # code = 123456

        # Check code
        if code != "123456":
            return False

        # Update user password
        user = None
        if login.isdigit():
            user = self.getUserByEmail(login)
        if user:
            user.password = newPassword
            return True
        for userx in self.confirmedUsers:
            if userx.email == login:
                userx.password = newPassword
                return True
        return False

    def resendConfirmationCode(self, email: str) -> bool:
        user = self.getUserByEmail(email)

        if user is None:
            raise NonExistentUser(f"{email}")

        # Send email

        return True
