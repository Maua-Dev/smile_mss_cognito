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
            'login': '75599469093',
            'password': '123456',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 200
        assert response.body == {
            'access_token': f'validAccessToken-{75599469093}',
            'refresh_token': f'validRefreshToken-{75599469093}',
            'role': ROLE.STUDENT.value,
            'access_level': ACCESS_LEVEL.USER.value,
            'cpf_rne': '75599469093',
            'email': 'bruno@bruno.com'
        }

    @pytest.mark.asyncio
    async def test_login_invalid_user_controller(self):
        request = HttpRequest(body={
            'login': '75599469093',
            'password': '1234567',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_login_non_existent_user_controller(self):
        request = HttpRequest(body={
            'login': '19971667045',
            'password': '123456',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 400



