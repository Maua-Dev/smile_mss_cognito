import pytest

from src.adapters.controllers.change_password_controller import ChangePasswordController
from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ChangePasswordController:

    @pytest.mark.asyncio
    async def test_change_valid_cpfRne_controller(self):
        request = HttpRequest(body={
            'login': 12345678910
        })

        changePasswordController = ChangePasswordController(UserRepositoryMock())
        response = await changePasswordController(request)
        assert response.status_code == 200
        assert response.body == {
            'result': True,
            'message': ''
        }

    @pytest.mark.asyncio
    async def test_change_valid_email_controller(self):
        request = HttpRequest(body={
            'login': "user2@user.com"
        })

        changePasswordController = ChangePasswordController(UserRepositoryMock())
        response = await changePasswordController(request)
        assert response.status_code == 200
        assert response.body == {
            'result': True,
            'message': ''
        }

    @pytest.mark.asyncio
    async def test_change_non_existent_cpfRne_controller(self):
        request = HttpRequest(body={
            'login': 12325698910
        })

        changePasswordController = ChangePasswordController(UserRepositoryMock())
        response = await changePasswordController(request)
        assert response.status_code == 400
        assert response.body == {
            'result': False,
            'message': 'User not found'
        }

    @pytest.mark.asyncio
    async def test_change_invalid_cpfRne_controller(self):
        request = HttpRequest(body={
            'login': 1232569856910
        })

        changePasswordController = ChangePasswordController(UserRepositoryMock())
        response = await changePasswordController(request)
        assert response.status_code == 400
        assert response.body == {
            'result': False,
            'message': 'User not found'
        }

    @pytest.mark.asyncio
    async def test_change_non_existent_cpfRne_controller(self):
        request = HttpRequest(body={
            'login': "teste@qualquercoisa.com"
        })

        changePasswordController = ChangePasswordController(UserRepositoryMock())
        response = await changePasswordController(request)
        assert response.status_code == 400
        assert response.body == {
            'result': False,
            'message': 'User not found'
        }





