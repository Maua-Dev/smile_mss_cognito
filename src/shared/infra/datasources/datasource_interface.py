from abc import ABC, abstractmethod
from typing import List

from src.infra.dtos.User.user_dto import UserDTO


class IDataSource(ABC):
    @abstractmethod
    def getAllUsers(self, userId: int) -> List[UserDTO]:
        pass

    @abstractmethod
    def getUserById(self,codeSubject: str) -> UserDTO:
        pass