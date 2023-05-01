from src.modules.change_password.app.change_password_controller import ChangePasswordController
from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="change_password")

class Test_ChangePasswordController:

    def test_change_password_controller(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo, observability=observability)
        controller = ChangePasswordController(usecase, observability=observability)

        response = controller(HttpRequest(body={'email': 'zeeba@gmail.com'}))

        assert response.status_code == 200
        assert response.body == {'result': True, 'message': ''}

    def test_change_password_missing_email(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo, observability=observability)
        controller = ChangePasswordController(usecase, observability=observability)

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert response.body == "Não existe corpo da requisição."

    def test_change_password_entity_error(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo, observability=observability)
        controller = ChangePasswordController(usecase, observability=observability)

        response = controller(HttpRequest(
            body={'email': 'invalid_email'}))

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: email'
