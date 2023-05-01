from src.modules.confirm_user_creation.app.confirm_user_creation_controller import ConfirmUserCreationController
from src.modules.confirm_user_creation.app.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="confirm_user_creation")

class Test_ConfirmUserCreationController:

    def test_confirm_user_creation_controller(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo, observability=observability)
        controller = ConfirmUserCreationController(usecase, observability=observability)

        body = {"email": "joao@gmail.com", "confirmation_code": "102030"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 303
        assert response.headers == {
            "location": 'None/#/login/cadastro/sucesso'
        }

    def test_confirm_user_creation_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo, observability=observability)
        controller = ConfirmUserCreationController(usecase, observability=observability)

        body = {"email": "joaogmail.com", "confirmation_code": "102030"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.body == 'Nenhum usuário encontrado'
        assert response.status_code == 404

    def test_confirm_user_creation_controller_invalid_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo, observability=observability)
        controller = ConfirmUserCreationController(usecase, observability=observability)

        body = {"email": "joao@gmail.com", "confirmation_code": "123456"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 403
        assert response.body == 'Código de confirmção inválido'

    def test_confirm_user_creation_controller_already_confirmed(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo, observability=observability)
        controller = ConfirmUserCreationController(usecase, observability=observability)

        body = {"email": "zeeba@gmail.com", "confirmation_code": "102030"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 403
        assert response.body == 'Usuário já confirmado'

    def test_confirm_user_creation_controller_already_confirmed_and_invalid_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo, observability=observability)
        controller = ConfirmUserCreationController(usecase, observability=observability)

        body = {"email": "zeeba@gmail.com", "confirmation_code": "123456"}
        request = HttpRequest(body)

        response = controller(request)
        assert response.status_code == 403
        assert response.body == 'Usuário já confirmado'
