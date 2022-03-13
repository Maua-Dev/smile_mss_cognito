from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    async def getUserByCpfRne(self, cpfRne: int) -> User:
        pass

    @abstractmethod
    async def getAllUsers(self) -> List[User]:
        pass

    @abstractmethod
    async def createUser(self, user: User) -> int:
        pass

    @abstractmethod
    async def updateUser(self, user: User):
        pass

    @abstractmethod
    async def deleteUser(self, userCpfRne: int):
        pass

    @abstractmethod
    async def confirmUserCreation(self, user: User, code: int):
        pass

    @abstractmethod
    async def loginUser(self, cpfRne: int, password: str) -> dict:  # accessToken, refreshToken
        pass

    @abstractmethod
    async def checkToken(self, cpfRne: int, token: str):
        pass

    @abstractmethod
    async def refreshToken(self, refreshToken: str) -> (str, str):  # accessToken, refreshToken
        pass
