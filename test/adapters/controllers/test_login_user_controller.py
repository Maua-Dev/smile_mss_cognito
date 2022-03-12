import pytest

from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_LoginUserController:

    @pytest.mark.asyncio
    async def test_login_valid_user_controller(self):
        request = HttpRequest(body={
            'cpfRne': 12345678910,
            'password': '123456',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 200
        assert response.body == {
            'token': f'validToken-{12345678910}'
        }

    @pytest.mark.asyncio
    async def test_login_invalid_user_controller(self):
        request = HttpRequest(body={
            'cpfRne': 12345678910,
            'password': '1234567',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_login_non_existent_user_controller(self):
        request = HttpRequest(body={
            'cpfRne': 12345678918,
            'password': '123456',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 400



