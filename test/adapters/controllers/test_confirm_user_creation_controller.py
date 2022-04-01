import pytest

from src.adapters.controllers.change_password_controller import ChangePasswordController
from src.adapters.controllers.confirm_change_password_controller import ConfirmChangePasswordController
from src.adapters.controllers.confirm_user_creation_controller import ConfirmUserCreationController
from src.adapters.controllers.login_user_controller import LoginUserController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ConfirmChangePasswordController:

    @pytest.mark.asyncio
    async def test_change_valid_cpfRne_controller(self):
        request = HttpRequest(body={
            'login': '54134054052',
            'code': '1234567'
        })

        repository = UserRepositoryMock()
        confirmUserCreationController = ConfirmUserCreationController(repository)
        response = await confirmUserCreationController(request)
        assert response.status_code == 200
        u = await repository.getUserByCpfRne('54134054052')
        assert u.name == 'User3'