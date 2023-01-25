import pytest

from src.modules.change_password.app.change_password_controller import ChangePasswordController
from src.modules.confirm_change_password.app.confirm_change_password_controller import ConfirmChangePasswordController
from src.modules.login_user.app.login_user_controller import LoginUserController
from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ChangePasswordController:

    @pytest.mark.asyncio
    async def test_change_valid_cpfRne_controller(self):
        request = HttpRequest(body={
            'login': '75599469093',
            'new_password': 'teste!!!123',
            'confirmation_code': '123456'
        })

        repository = UserRepositoryMock()
        confirmChangePasswordController = ConfirmChangePasswordController(
            repository)
        response = await confirmChangePasswordController(request)
        assert response.status_code == 200
        assert response.body == {
            'result': True,
            'message': ''
        }
        u = await repository.getUserByCpfRne('75599469093')
        assert u.password == 'teste!!!123'

    @pytest.mark.asyncio
    async def test_change_valid_email_controller(self):
        request = HttpRequest(body={
            'login': "user2@user.com",
            'new_password': 'teste!!!123',
            'confirmation_code': '123456'
        })

        repository = UserRepositoryMock()
        confirmChangePasswordController = ConfirmChangePasswordController(
            repository)
        response = await confirmChangePasswordController(request)
        assert response.status_code == 200
        assert response.body == {
            'result': True,
            'message': ''
        }
        u = await repository.getUserByCpfRne('64968222041')
        assert u.password == 'teste!!!123'

    @pytest.mark.asyncio
    async def test_change_non_existent_cpfRne_controller(self):
        request = HttpRequest(body={
            'login': 15418,
            'new_password': 'teste!!!123',
            'confirmation_code': '123456'
        })

        repository = UserRepositoryMock()
        confirmChangePasswordController = ConfirmChangePasswordController(
            repository)
        response = await confirmChangePasswordController(request)
        assert response.status_code == 400
        assert response.body == {
            'result': False,
            'message': 'User not found, invalid confirmation code or weak new password.'
        }
