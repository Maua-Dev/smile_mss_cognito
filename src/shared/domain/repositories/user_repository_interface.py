from abc import ABC, abstractmethod
from typing import List, Tuple
from src.shared.domain.entities.user import User


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
    # accessToken, refreshToken #todo change to login
    async def loginUser(self, login: str, password: str) -> dict:
        pass

    @abstractmethod
    async def checkToken(self, token: str) -> dict:  # user data
        pass

    @abstractmethod
    # accessToken, refreshToken
    async def refreshToken(self, refreshToken: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    async def changePassword(self, login: str) -> bool:
        pass

    @abstractmethod
    async def confirmChangePassword(self, login: str, newPassword: str, code: str) -> bool:
        pass
