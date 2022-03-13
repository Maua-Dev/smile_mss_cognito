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
            User(name='user1', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com", password="123456"
             ),
            User(name='user2', cpfRne=12345678911, ra=20001231, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), password="123456"
             )
        ]

    async def getAllUsers(self) -> List[User]:
        if len(self._users) > 0:
            return self._users, len(self._users)
        else:
            return None, 0

    async def getUserByCpfRne(self, cpfRne: int) -> User:
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

    async def deleteUser(self, cpfRne: int):
        cont = 0
        for userx in self._users:
            if userx.cpfRne == cpfRne:
                self._users.pop(cont)
                break
            cont += 1

    async def loginUser(self, cpfRne: int, password: str) -> dict:
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

    async def checkToken(self, cpfRne: int, token: str):
        splitToken = token.split("-")
        if len(splitToken) != 2:
            return False
        if splitToken[0] != "validToken":
            return False
        if splitToken[1] != str(cpfRne):
            return False
        return True

    async def refreshToken(self, refreshToken: str) -> (str, str):
        splitToken = refreshToken.split("-") # token, cpf
        if len(splitToken) != 2:
            return None, None
        if splitToken[0] != "validRefreshToken":
            return None, None
        if await self.getUserByCpfRne(int(splitToken[1])) is None:
            return None, None
        return "validAccessToken-" + splitToken[1], refreshToken
