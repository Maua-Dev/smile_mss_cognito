from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class CheckTokenUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, token: str) -> dict:

        data = self.repo.check_token(token)

        if not data:
            raise ForbiddenAction('Invalid Token')

        return data
