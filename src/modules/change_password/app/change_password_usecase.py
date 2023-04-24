from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class ChangePasswordUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, email: str) -> bool:
        self.observability.log_usecase_in()

        if not User.validate_email(email):
            raise EntityError('email')

        data = self.repo.change_password(email)

        if not data:
            pass
        self.observability.log_usecase_out()

        return data
