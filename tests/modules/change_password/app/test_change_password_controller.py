from src.modules.change_password.app.change_password_controller import ChangePasswordController
from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ChangePasswordController:

    def test_change_password_controller(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo)
        controller = ChangePasswordController(usecase)

        response = controller(HttpRequest(body={'email': 'zeeba@gmail.com'}))

        assert response.status_code == 200
        assert response.body == {'result': True, 'message': ''}

    def test_change_password_missing_email(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo)
        controller = ChangePasswordController(usecase)

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert response.body == 'Missing body.'

    def test_change_password_entity_error(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo)
        controller = ChangePasswordController(usecase)

        response = controller(HttpRequest(
            body={'email': 'invalid_email'}))

        assert response.status_code == 400
        assert response.body == 'Field email is not valid'
