from src.modules.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserController:

    def test_delete_user_controller(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)
        controller = DeleteUserController(usecase)

        body = {"email": "zeeba@gmail.com"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 200
        assert response.body == 'User deleted.'

    def test_delete_user_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)
        controller = DeleteUserController(usecase)

        body = {"email": "joaogmail.com"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 403
        assert response.body == 'That action is forbidden for this "User not found"'

    def test_delete_user_controller_user_unconfirmed(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo)
        controller = DeleteUserController(usecase)

        body = {"email": "joao@gmail.com"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 403
        assert response.body == 'That action is forbidden for this "User not found"'
