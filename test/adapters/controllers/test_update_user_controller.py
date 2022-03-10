from datetime import datetime

import pytest

from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class TestCreateUserController:
    mockUser = {
        "name": 'user1',
        "cpfRne": 12345678910,
        "ra": 19003315,
        "role": ROLE.STUDENT,
        "accessLevel": ACCESS_LEVEL.USER,
        "createdAt": datetime(2022, 3, 8, 22, 10),
        "email": "bruno@bruno.com",
        "updatedAt": datetime(2022, 3, 8, 22, 15)
    }


    @pytest.mark.asyncio
    async def test_update_valid_user_controller(self):
        u = self.mockUser.copy()
        u['name'] = "Bruno"
        u['email'] = "bruno@teste.com"
        request = HttpRequest(body=u)

        updateUserController = UpdateUserController(UserRepositoryMock())
        response = await updateUserController(request)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_invalid_cpfRne_user_controller(self):
        u = self.mockUser.copy()
        u['cpfRne'] = 12345678

        request = HttpRequest(body=u)

        updateUserController = UpdateUserController(UserRepositoryMock())
        response = await updateUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_update_valid_cpfRne_user_controller(self):
        u = self.mockUser.copy()
        u['cpfRne'] = 12345678615

        request = HttpRequest(body=u)

        updateUserController = UpdateUserController(UserRepositoryMock())
        response = await updateUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_update_invalid_email_user_controller(self):
        u = self.mockUser.copy()
        u['email'] = 'teste@'

        request = HttpRequest(body=u)

        updateUserController = UpdateUserController(UserRepositoryMock())
        response = await updateUserController(request)
        assert response.status_code == 400
