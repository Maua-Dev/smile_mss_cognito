from datetime import datetime

import pytest

from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUpdateUserController:

    @pytest.mark.asyncio
    async def test_update_valid_user_controller(self):
        req = {
            "name": 'Bruno',
            "social_name": 'userx1',
            "certificate_with_social_name": 'true',
        }
        header = {"Authorization": "Bearer validAccessToken-75599469093"}
        request = HttpRequest(body=req, headers=header)

        updateUserController = UpdateUserController(UserRepositoryMock())
        response = await updateUserController(request)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_invalid_user_controller(self):
        req = {
            "name": 'Bruno',
            "social_name": 'userx1',
            "certificate_with_social_name": True,
        }
        header = {"Authorization": "Bearer validAccessToken-75599469053"}
        request = HttpRequest(body=req, headers=header)

        updateUserController = UpdateUserController(UserRepositoryMock())
        response = await updateUserController(request)
        assert response.status_code == 400
