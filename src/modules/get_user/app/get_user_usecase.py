from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetUserUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, email: str) -> User:
        self.observability.log_usecase_in()

        if not User.validate_email(email):
            raise EntityError('email')

        user = self.repo.get_user_by_email(email=email)

        if user is None:
            raise NoItemsFound('user')
        self.observability.log_usecase_out()

        return user
