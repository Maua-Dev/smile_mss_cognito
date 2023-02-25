from src.modules.check_token.app.check_token_controller import CheckTokenController
from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CheckTokenController:

    def test_check_token_controller(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)
        controller = CheckTokenController(usecase)

        header = {"Authorization": "Bearer valid_access_token-zeeba@gmail.com"}
        request = HttpRequest(headers=header)

        response = controller(request)
        assert response.status_code == 200
        assert response.body == {
            'role': ROLE.STUDENT.value,
            'access_level': ACCESS_LEVEL.USER.value,
            'email': 'zeeba@gmail.com',
            'valid_token': True,
            'user_id': '000000000000000000000000000000000001'
        }

    def test_check_token_controller_invalid_token(self):
        repo = UserRepositoryMock()
        usecase = CheckTokenUsecase(repo)
        controller = CheckTokenController(usecase)

        header = {"Authorization": "Bearer INVALID_access_token-zeeba@gmail.com"}
        request = HttpRequest(headers=header)

        response = controller(request)
        assert response.status_code == 400
        assert response.body == {
            'valid_token': False,
            'error_message': "Parâmetro inválido: access_token"
        }
