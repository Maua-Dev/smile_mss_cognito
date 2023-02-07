
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class ConfirmUserCreationUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, confirmation_code: str) -> bool:

        result = self.repo.confirm_user_creation(email, confirmation_code)

        return result
