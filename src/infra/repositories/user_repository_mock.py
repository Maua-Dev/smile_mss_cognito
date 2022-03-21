from datetime import datetime
from typing import List

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError, InvalidToken, UserAlreadyExists
from src.domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):

    def __init__(self) -> None:
        super().__init__()
        self._users = [
            User(name='user1', cpfRne='75599469093', ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com", password="123456"
                 ),
            User(name='user2', cpfRne='64968222041', ra=20001231, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), password="123456", email="user2@user.com"
                 )
        ]

    async def getAllUsers(self) -> List[User]:
        if len(self._users) > 0:
            return self._users, len(self._users)
        else:
            return None, 0

    async def getUserByCpfRne(self, cpfRne: str) -> User:
        user: User = None
        for userx in self._users:
            if userx.cpfRne == cpfRne:
                user = userx
                break
            pass
        return user

    async def checkUserByPropriety(self, propriety: str, value: str) -> bool:
        for userx in self._users:
            if getattr(userx, propriety) == value and value != None:
                return True
        return False

    async def createUser(self, user: User):
        duplicitySensitive = ['cpfRne', 'email', 'ra']
        for field in duplicitySensitive:
            if await self.checkUserByPropriety(propriety=field, value=getattr(user, field)):
                raise UserAlreadyExists(f'Propriety ${field} = "${getattr(user, field)}" already exists')
        self._users.append(user)

    async def confirmUserCreation(self, user: User, code: int):
        pass

    async def updateUser(self, user: User):
        cont = 0
        for userx in self._users:
            if userx.cpfRne == user.cpfRne:
                break
            cont += 1

        self._users[cont] = user

    async def deleteUser(self, cpfRne: str):
        cont = 0
        for userx in self._users:
            if userx.cpfRne == cpfRne:
                self._users.pop(cont)
                break
            cont += 1

    async def loginUser(self, cpfRne: str, password: str) -> dict:
        u = await self.getUserByCpfRne(cpfRne)
        if u is None:
            return None
        if u.password == password:
            dictResponse = u.dict()
            dictResponse.pop('password')
            dictResponse["accessToken"] = "validAccessToken-" + str(cpfRne)
            dictResponse["refreshToken"] = "validRefreshToken-" + str(cpfRne)
            return dictResponse
        return None

    async def checkToken(self, token: str) -> dict:
        splitToken = token.split("-")
        if len(splitToken) != 2:
            return None
        if splitToken[0] != "validAccessToken":
            return None

        cpfRne = splitToken[1]
        user = await self.getUserByCpfRne(cpfRne)
        if user is None:
            return None
        data = user.dict()
        data.pop('password')
        return data

    async def refreshToken(self, refreshToken: str) -> (str, str):
        splitToken = refreshToken.split("-")  # token, cpf
        if len(splitToken) != 2:
            return None, None
        if splitToken[0] != "validRefreshToken":
            return None, None
        if await self.getUserByCpfRne(splitToken[1]) is None:
            return None, None
        return "validAccessToken-" + splitToken[1], refreshToken

    async def changePassword(self, login: str) -> bool:
        user = None
        if login.isdigit():
            user = await self.getUserByCpfRne(login)
        if user:
            return True

        for userx in self._users:
            if userx.email == login:
                return True
        return False



    async def confirmChangePassword(self, login: str, newPassword: str, code: str) -> bool:
        # code = 123456

        # Check code
        if code != "123456":
            return False

        # Update user password
        user = None
        if login.isdigit():
            user = await self.getUserByCpfRne(login)
        if user:
            user.password = newPassword
            return True
        for userx in self._users:
            if userx.email == login:
                userx.password = newPassword
                return True
        return False



