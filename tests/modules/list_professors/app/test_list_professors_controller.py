from src.modules.list_professors.app.list_professor_controller import ListProfessorsController
from src.modules.list_professors.app.list_professors_usecase import ListProfessorsUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="list_professors")


class Test_ListProfessorsController:
    def test_list_professors(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        controller = ListProfessorsController(usecase, observability=observability)

        request = HttpRequest(
            headers={'Authorization': 'Bearer ' + 'valid_access_token-' + repo.confirmed_users[1].email}
        )

        list_professors = controller(request=request)

        assert list_professors.status_code == 200
        assert list_professors.body['message'] == 'the professors were retrieved'

    def test_list_professors_missing_access_token(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        controller = ListProfessorsController(usecase, observability=observability)

        request = HttpRequest(
            headers={}
        )

        list_professors = controller(request=request)

        assert list_professors.status_code == 400
        assert list_professors.body == f'Parâmetros ausentes: Authorization header'

    def test_list_professors_invalid_access_token(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        controller = ListProfessorsController(usecase, observability=observability)

        request = HttpRequest(
            headers={'Authorization': 'Bearer ' + 'invalid_access_token'}
        )

        list_professors = controller(request=request)

        assert list_professors.status_code == 400
        assert list_professors.body == f'Parâmetro inválido: access_token'

    def test_list_professor_not_found(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        controller = ListProfessorsController(usecase, observability=observability)

        request = HttpRequest(
            headers={'Authorization': 'Bearer ' + 'valid_access_token-emailfalso@maua.br'}
        )

        list_professors = controller(request=request)

        assert list_professors.status_code == 404
        assert list_professors.body == f'Usuário não encontrado'

    def test_list_professors_not_admin(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        controller = ListProfessorsController(usecase, observability=observability)

        request = HttpRequest(
            headers={'Authorization': 'Bearer ' + 'valid_access_token-zeeba@gmail.com'}
        )

        list_professors = controller(request=request)

        assert list_professors.status_code == 403
        assert list_professors.body == f'Apenas administradores podem acessar essa funcionalidade'






