from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    async def getUserByCpfRne(self, cpfRne: int) -> User:
        pass

    @abstractmethod
    def getAllUsers(self) -> List[User]:
        pass

    @abstractmethod
    async def checkUserByPropriety(self, propriety: str, value: str) -> bool:
        pass

    @abstractmethod
    async def createUser(self, user: User):
        pass
