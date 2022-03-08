from typing import List
from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError
from src.domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):
    def __init__(self) -> None:
        super().__init__()
        self._users = [
            User(name='user1', cpfRne=12345678910, role='student'),
            User(name='user2', cpfRne=12345678911, role='admin'),
        ]

    def getAllUsers(self) -> List[User]:
        if len(self._users) > 0:
            return self._users, len(self._users)
        else:
            return None, 0

    async def getUserByCpfRne(self, cpfRne: int) -> User:
        user: User = None
        for userx in self._users:
            if userx.cpfRne == cpfRne:
                user = userx
        return user
