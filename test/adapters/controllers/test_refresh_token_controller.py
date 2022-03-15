import pytest

from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.refresh_token_controller import RefreshTokenController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_RefreshTokenController:

    @pytest.mark.asyncio
    async def test_refresh_valid_token_controller(self):
        header = {"Authorization": "Bearer validRefreshToken-12345678910"}
        request = HttpRequest(headers=header)

        refreshTokenController = RefreshTokenController(UserRepositoryMock())
        response = await refreshTokenController(request)
        assert response.status_code == 200
        assert response.body == {
            'access_token': f'validAccessToken-{12345678910}',
            'refresh_token': f'validRefreshToken-{12345678910}'
        }

    @pytest.mark.asyncio
    async def test_login_invalid_token_controller(self):
        header = {"Authorization": "Bearer invalidRefreshToken-12345678910"}
        request = HttpRequest(headers=header)

        refreshTokenController = RefreshTokenController(UserRepositoryMock())
        response = await refreshTokenController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_login_non_existent_user_token_controller(self):
        header = {"Authorization": "Bearer validRefreshToken-12345678918"}
        request = HttpRequest(headers=header)

        refreshTokenController = RefreshTokenController(UserRepositoryMock())
        response = await refreshTokenController(request)
        assert response.status_code == 400



