from typing import Tuple
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class RefreshTokenUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, refresh_token: str) -> Tuple[str, str]:
        self.observability.log_usecase_in()
        
        tokens = self.repo.refresh_token(refresh_token)
        if tokens is None or tokens == (None, None):
            raise ForbiddenAction(f'Refresh Token: {refresh_token}')

        access_token, refresh_token, id_token = tokens
        if access_token is None or refresh_token is None:
            raise ForbiddenAction(f'Refresh Token or Access Token')
        self.observability.log_usecase_out()
        
        return access_token, refresh_token, id_token
