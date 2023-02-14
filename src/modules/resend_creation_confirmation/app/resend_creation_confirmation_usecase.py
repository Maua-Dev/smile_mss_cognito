from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class ResendCreationConfirmationUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str) -> bool:
        if not User.validate_email(email):
            raise EntityError("email")

        result = self.repo.resend_confirmation_code(email)

        return result
