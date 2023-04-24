from typing import List

from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class ListProfessorsUsecase:
    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.observability = observability

    def __call__(self) -> List[User]:
        self.observability.log_usecase_in()
        
        professors_response = self.repo.list_professors()
        self.observability.log_usecase_out()
        
        return professors_response
