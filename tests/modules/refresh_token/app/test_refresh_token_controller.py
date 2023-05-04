from src.modules.refresh_token.app.refresh_token_controller import RefreshTokenController
from src.modules.refresh_token.app.refresh_token_usecase import RefreshTokenUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="refresh_token")

class Test_RefreshTokenController:
    def test_refresh_token_controller(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)
        controller = RefreshTokenController(usecase, observability=observability)

        header = {"Authorization": "Bearer valid_refresh_token-vitor@maua.br"}
        request = HttpRequest(headers=header)

        response = controller(request)

        assert response.status_code == 200
        assert response.body['access_token'] == "valid_access_token-vitor@maua.br"
        assert response.body['refresh_token'] == "valid_refresh_token-vitor@maua.br"
        assert response.body['id_token'] == "valid_id_token-vitor@maua.br"
        assert response.body['message'] == "Token refreshed successfully"

    def test_refresh_token_controller_missing_authorization(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)
        controller = RefreshTokenController(usecase, observability=observability)

        request = HttpRequest()

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: Authorization header'

    def test_refresh_token_controller_invalid_authorization(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)
        controller = RefreshTokenController(usecase, observability=observability)

        header = {"Authorization": "Bearervalid_refresh_token-vitor@maua.br"}
        request = HttpRequest(headers=header)

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: access_token'

    def test_refresh_token_controller_invalid_refresh_token(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)
        controller = RefreshTokenController(usecase, observability=observability)

        headers = {"Authorization": "Bearer invalid_refresh_token-vitor@maua.br"}

        request = HttpRequest(headers=headers)
        reponse = controller(request)

        assert reponse.status_code == 403
        assert reponse.body == 'Sem autorização para: Refresh Token: invalid_refresh_token-vitor@maua.br'

    def test_refresh_token_controller_invalid_refresh_token_or_access_token(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)
        controller = RefreshTokenController(usecase, observability=observability)

        headers = {"Authorization": "Bearer valid_refresh_token-vitor@maua.com"}

        request = HttpRequest(headers=headers)
        reponse = controller(request)

        assert reponse.status_code == 403
        assert reponse.body == "Sem autorização para: Refresh Token: valid_refresh_token-vitor@maua.com"





