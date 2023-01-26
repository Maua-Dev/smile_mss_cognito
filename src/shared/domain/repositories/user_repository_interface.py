from abc import ABC, abstractmethod
from typing import List, Tuple
from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> int:
        pass

    @abstractmethod
    async def update_user(self, user: User):
        pass

    @abstractmethod
    async def delete_user(self, cpfRne: int):
        pass

    @abstractmethod
    async def confirm_user_creation(self, login: str, code: int):
        pass

    @abstractmethod
    # accessToken, refreshToken #todo change to login
    async def login_user(self, login: str, password: str) -> dict:
        pass

    @abstractmethod
    async def check_token(self, token: str) -> dict:  # user data
        pass

    @abstractmethod
    # accessToken, refreshToken
    async def refresh_token(self, refreshToken: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    async def change_password(self, login: str) -> bool:
        pass

    @abstractmethod
    async def confirm_change_password(self, login: str, newPassword: str, code: str) -> bool:
        pass
