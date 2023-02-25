from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, UserNotConfirmed


class DeleteUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: int):

        user = self.repo.get_user_by_email(email)
        if not user:
            raise UserNotConfirmed("user")

        self.repo.delete_user(email)

        return True
