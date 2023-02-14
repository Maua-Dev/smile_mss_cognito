from src.modules.list_professors.app.list_professors_usecase import ListProfessorsUsecase
from src.shared.domain.entities.enums import ROLE
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListProfessorsUsecase():
    def test_list_professors(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo)
        professors = usecase()

        assert len(professors) == 1
        assert all([user.role == ROLE.PROFESSOR for user in professors])
