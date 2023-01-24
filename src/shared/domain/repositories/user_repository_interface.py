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
    async def deleteUser(self, cpfRne: int):
        pass

    @abstractmethod
    async def confirmUserCreation(self, login: str, code: int):
        pass

    @abstractmethod
    async def loginUser(self, login: str, password: str) -> dict:  # accessToken, refreshToken #todo change to login
        pass

    @abstractmethod
    async def checkToken(self, token: str) -> dict: # user data
        pass

    @abstractmethod
    async def refreshToken(self, refreshToken: str) -> (str, str):  # accessToken, refreshToken
        pass

    @abstractmethod
    async def changePassword(self, login: str) -> bool:
        pass

    @abstractmethod
    async def confirmChangePassword(self, login: str, newPassword:str, code: str) -> bool:
        pass
