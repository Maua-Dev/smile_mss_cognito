from typing import List

from src.shared.domain.entities.enums import ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction


class ListProfessorsUsecase:
    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self, access_token: str) -> List[User]:
        self.observability.log_usecase_in()

        user_requester_data = self.repo.check_token(access_token)

        if user_requester_data is None:
            raise NoItemsFound("user")

        user_requester = User.parse_object(user_requester_data)

        if user_requester.access_level != ACCESS_LEVEL.ADMIN:
            raise ForbiddenAction("user")

        professors_response = self.repo.list_professors()
        self.observability.log_usecase_out()
        
        return professors_response
