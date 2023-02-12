from src.modules.list_professors.app.list_professor_controller import ListProfessorsController
from src.modules.list_professors.app.list_professors_usecase import ListProfessorsUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListProfessorsController:
    def test_list_professors(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo)
        controller = ListProfessorsController(usecase)

        request = HttpRequest()

        list_professors = controller(request=request)

        assert list_professors.status_code == 200
        assert list_professors.body['message'] == 'the professors were retrieved'

