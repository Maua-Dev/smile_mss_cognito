from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidCredentials


class LoginUserUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, email: str, password: str) -> dict:
        self.observability.log_usecase_in()
        
        login_response_fields = ['email', 'access_token',
                                 'refresh_token', 'email', 'role', 'access_level']

        if not User.validate_email(email):
            raise EntityError('email')

        if not User.validate_password(password):
            raise EntityError('password')

        data = self.repo.login_user(email, password)
        if data is None:
            raise InvalidCredentials("email or password")
        if not set(login_response_fields) <= set(data.keys()):
            raise MissingParameters(f'{login_response_fields}')
        
        self.observability.log_usecase_out()
        
        return data
