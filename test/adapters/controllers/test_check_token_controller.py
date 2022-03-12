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
        request = HttpRequest(body={
            'cpfRne': 12345678910,
            'token': 'validToken-12345678910',
        })

        checkTokenController = CheckTokenController(UserRepositoryMock())
        response = await checkTokenController(request)
        assert response.status_code == 200
        assert response.body == {
            'tokenValidated': True
        }

    @pytest.mark.asyncio
    async def test_check_token_invalid_token_controller(self):
        request = HttpRequest(body={
            'cpfRne': 12345678910,
            'token': 'validToken-12345678914',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 400

