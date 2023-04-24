
from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class ConfirmUserCreationUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, email: str, confirmation_code: str) -> bool:
        self.observability.log_usecase_in()

        result = self.repo.confirm_user_creation(email, confirmation_code)
        self.observability.log_usecase_out()

        return result
