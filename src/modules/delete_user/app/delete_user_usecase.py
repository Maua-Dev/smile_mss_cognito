from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, UserNotConfirmed


class DeleteUserUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, email: int):
        self.observability.log_usecase_in()

        user = self.repo.get_user_by_email(email)
        if not user:
            raise UserNotConfirmed("user")

        self.repo.delete_user(email)
        self.observability.log_usecase_out()

        return True
