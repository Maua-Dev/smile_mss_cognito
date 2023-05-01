from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class ConfirmChangePasswordUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, email: str, new_password: str, confirmation_code: str) -> bool:
        self.observability.log_usecase_in()

        result = self.repo.confirm_change_password(
            email, new_password, confirmation_code
        )
        
        self.observability.log_usecase_out()

        if not result:
            pass

        return result
