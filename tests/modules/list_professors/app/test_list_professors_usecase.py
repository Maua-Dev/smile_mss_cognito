from src.modules.list_professors.app.list_professors_usecase import ListProfessorsUsecase
from src.shared.domain.entities.enums import ROLE
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="list_professors")

class Test_ListProfessorsUsecase():
    def test_list_professors(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        professors = usecase()

        assert len(professors) == 1
        assert all([user.role == ROLE.PROFESSOR for user in professors])
