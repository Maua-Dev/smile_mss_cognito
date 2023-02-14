from src.shared.domain.entities.enums import ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class CreateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: User) -> User:

        if user.access_level != ACCESS_LEVEL.USER:
            raise EntityError('access_level')

        user.email = user.email.lower()

        return self.repo.create_user(user)
