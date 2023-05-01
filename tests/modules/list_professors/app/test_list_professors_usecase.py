import pytest

from src.modules.list_professors.app.list_professors_usecase import ListProfessorsUsecase
from src.shared.domain.entities.enums import ROLE
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="list_professors")

class Test_ListProfessorsUsecase():
    def test_list_professors(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        professors = usecase("valid_access_token-vitor@maua.br")

        assert len(professors) == 1
        assert all([user.role == ROLE.PROFESSOR for user in professors])

    def test_list_professors_not_found(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)

        with pytest.raises(NoItemsFound):
            professors = usecase("valid_access_token-emailfalso@maua.br")

    def test_list_professors_not_admin(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)

        with pytest.raises(ForbiddenAction):
            professors = usecase("valid_access_token-zeeba@gmail.com")


