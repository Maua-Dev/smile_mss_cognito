from src.modules.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="delete_user")

class Test_DeleteUserController:

    def test_delete_user_controller(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo, observability=observability)
        controller = DeleteUserController(usecase, observability=observability)

        body = {"email": "zeeba@gmail.com"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 200
        assert response.body == 'User deleted.'

    def test_delete_user_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo, observability=observability)
        controller = DeleteUserController(usecase, observability=observability)

        body = {"email": "joaogmail.com"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 401
        assert response.body == 'Usuário não confirmado'

    def test_delete_user_controller_user_unconfirmed(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo, observability=observability)
        controller = DeleteUserController(usecase, observability=observability)

        body = {"email": "joao@gmail.com"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 401
        assert response.body == "Usuário não confirmado"
