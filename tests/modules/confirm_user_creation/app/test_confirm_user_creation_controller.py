from src.modules.confirm_user_creation.app.confirm_user_creation_controller import ConfirmUserCreationController
from src.modules.confirm_user_creation.app.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ConfirmUserCreationController:

    def test_confirm_user_creation_controller(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)
        controller = ConfirmUserCreationController(usecase)

        body = {"email": "joao@gmail.com", "confirmation_code": "102030"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 303
        assert response.headers == {
            "location": "https://static.vecteezy.com/ti/fotos-gratis/t2/2883331-macaco-sentado-na-parede-gratis-foto.jpg"
        }

    def test_confirm_user_creation_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)
        controller = ConfirmUserCreationController(usecase)

        body = {"email": "joaogmail.com", "confirmation_code": "102030"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 500
        assert response.body == 'That action is forbidden for this "User not found".'

    def test_confirm_user_creation_controller_invalid_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)
        controller = ConfirmUserCreationController(usecase)

        body = {"email": "joao@gmail.com", "confirmation_code": "123456"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 500
        assert response.body == 'That action is forbidden for this "Invalid Confirmation Code".'

    def test_confirm_user_creation_controller_already_confirmed(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)
        controller = ConfirmUserCreationController(usecase)

        body = {"email": "zeeba@gmail.com", "confirmation_code": "102030"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 500
        assert response.body == 'That action is forbidden for this "User already confirmed".'

    def test_confirm_user_creation_controller_already_confirmed_and_invalid_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)
        controller = ConfirmUserCreationController(usecase)

        body = {"email": "zeeba@gmail.com", "confirmation_code": "123456"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 500
        assert response.body == 'That action is forbidden for this "User already confirmed".'
