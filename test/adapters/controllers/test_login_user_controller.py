import pytest

from src.modules.login_user.app.login_user_controller import LoginUserController
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
            'email': 'bruno@bruno.com',
            'social_name': 'Bruno',
            'name': 'User1',
            'certificate_with_social_name': True,
            'id': '1'
        }

    @pytest.mark.asyncio
    async def test_login_valid_user_controller_no_socialName(self):
        request = HttpRequest(body={
            'login': '64968222041',
            'password': '123456',
        })

        loginUserController = LoginUserController(UserRepositoryMock())
        response = await loginUserController(request)
        assert response.status_code == 200
        assert response.body == {
            'access_token': f'validAccessToken-{64968222041}',
            'refresh_token': f'validRefreshToken-{64968222041}',
            'role': ROLE.PROFESSOR.value,
            'access_level': ACCESS_LEVEL.ADMIN.value,
            'cpf_rne': '64968222041',
            'email': 'user2@user.com',
            'social_name': None,
            'name': 'User2',
            'certificate_with_social_name': False,
            'id': '2'
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
