from src.modules.resend_creation_confirmation.app.resend_creation_confirmation_controller import \
    ResendCreationConfirmationController
from src.modules.resend_creation_confirmation.app.resend_creation_confirmation_usecase import \
    ResendCreationConfirmationUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ResendCreationConfirmationController:

    def test_resend_confirmation_controller(self):
        repo = UserRepositoryMock()
        usecase = ResendCreationConfirmationUsecase(repo)
        controller = ResendCreationConfirmationController(usecase)

        request = HttpRequest(body={'email': 'vitor@maua.br'})

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {'message': 'the email was sent'}

    def test_resend_confirmation_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = ResendCreationConfirmationUsecase(repo)
        controller = ResendCreationConfirmationController(usecase)

        request = HttpRequest(body={})

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: email'

    def test_resend_confirmation_controller_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = ResendCreationConfirmationUsecase(repo)
        controller = ResendCreationConfirmationController(usecase)

        request = HttpRequest(body={'email': 'vitor@maua'})

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: email'

    def test_resend_confirmation_controller_nonexistent_email(self):
        repo = UserRepositoryMock()
        usecase = ResendCreationConfirmationUsecase(repo)
        controller = ResendCreationConfirmationController(usecase)

        request = HttpRequest(body={'email': 'vitor@gmail.com'})

        response = controller(request)

        assert response.status_code == 404
        assert response.body == 'Nenhum usuário encontrado com parâmetro: user email: vitor@gmail.com'
