import pytest

from src.adapters.controllers.check_token_controller import CheckTokenController
from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CheckTokenController:

    @pytest.mark.asyncio
    async def test_check_token_valid_token_controller(self):
        header = {"Authorization": "Bearer validAccessToken-75599469093"}
        request = HttpRequest(headers=header)

        checkTokenController = CheckTokenController(UserRepositoryMock())
        response = await checkTokenController(request)
        assert response.status_code == 200
        assert response.body == {
            'role': ROLE.STUDENT.value,
            'access_level': ACCESS_LEVEL.USER.value,
            'cpf_rne': '75599469093',
            'email': 'bruno@bruno.com',
            'valid_token': True
        }
    @pytest.mark.asyncio
    async def test_check_token_invalid_token_controller(self):
        header = {"Authorization": "Bearer invalidAccessToken-75599469093"}
        request = HttpRequest(headers=header)

        checkTokenController = CheckTokenController(UserRepositoryMock())
        response = await checkTokenController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_check_token_invalid_token_controller2(self):
        header = {"Authorization": "Random validAccessToken-75599469093"}
        request = HttpRequest(headers=header)

        checkTokenController = CheckTokenController(UserRepositoryMock())
        response = await checkTokenController(request)
        assert response.status_code == 400

