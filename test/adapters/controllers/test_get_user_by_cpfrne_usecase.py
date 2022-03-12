import pytest
from src.adapters.controllers.get_user_by_cpfrne_controller import GetUserByCpfRneController
from src.adapters.viewmodels.get_user_model import GetUserModel
from src.infra.repositories.user_repository_mock import UserRepositoryMock
from src.adapters.helpers.http_models import HttpRequest, NoContent, BadRequest
from src.domain.entities.user import User


class Test_GetUserByCpfRneController:

    @pytest.mark.asyncio
    async def test_get_user_by_cpfrne_controller(self):
        getUserByCpfrneController = GetUserByCpfRneController(UserRepositoryMock())
        req = HttpRequest(query={'cpfRne': '12345678910'})
        answer = await getUserByCpfrneController(req)

        assert type(answer.body) is GetUserModel
        assert answer.status_code == 200

    @pytest.mark.asyncio
    async def test_get_user_by_cpfrne_controller_no_item_found(self):
        getUserByCpfrneController = GetUserByCpfRneController(UserRepositoryMock())
        req = HttpRequest(query={'cpfRne': '12345678912'})
        answer = await getUserByCpfrneController(req)

        assert type(answer) is NoContent
        assert answer.status_code == 204

    @pytest.mark.asyncio
    async def test_get_user_by_cpfrne_controller_controller_error(self):
        getUserByCpfrneController = GetUserByCpfRneController(UserRepositoryMock())
        req = HttpRequest(query={'cpfRne': 'string'})
        answer = await getUserByCpfrneController(req)

        assert type(answer) is BadRequest
        assert answer.status_code == 400