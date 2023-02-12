from abc import ABC, abstractmethod
from typing import List, Tuple
from src.shared.domain.entities.user import User


class IUserRepository(ABC):

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        """
        Check if the user already exists, if not, create it and return it
        else raise DuplicatedItem
        """
        pass

    @abstractmethod
    def update_user(self, user_email: str, kvp_to_update: dict) -> User:
        pass

    @abstractmethod
    def delete_user(self, cpfRne: int):
        pass

    @abstractmethod
    def confirm_user_creation(self, email: str, confirmation_code: str) -> bool:
        pass

    @abstractmethod
    # accessToken, refreshToken #todo change to login
    def login_user(self, login: str, password: str) -> dict:
        pass

    @abstractmethod
    def check_token(self, token: str) -> dict:  # user data
        pass

    @abstractmethod
    # accessToken, refreshToken
    def refresh_token(self, refreshToken: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    def change_password(self, login: str) -> bool:
        pass

    @abstractmethod
    def confirm_change_password(self, login: str, newPassword: str, code: str) -> bool:
        pass

    @abstractmethod
    def resend_confirmation_code(self, email: str) -> bool:
        """
        Returns True if the email exists and the code was sent,
        else raise NoItemsFound
        """
        pass

    @abstractmethod
    def list_professors(self) -> List[User]:
        pass
