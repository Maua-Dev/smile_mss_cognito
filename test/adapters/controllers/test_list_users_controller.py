import pytest

from src.adapters.controllers.list_users_controller import ListUsersController
from src.adapters.helpers.http_models import HttpRequest
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersController:

    @pytest.mark.asyncio
    async def test_list_valid_users(self):
        repository = UserRepositoryMock()

        id1 = repository._confirmedUsers[0].id
        id2 = repository._confirmedUsers[1].id
        id3 = 54
        token = "Bearer validAccessToken-64968222041"

        req = HttpRequest(body=[id1, id2, id3], headers={'Authorization': token})

        listUsersUsecase = ListUsersController(repository)
        res = await listUsersUsecase(req)


        assert res.status_code == 200
        assert res.body[id1]["cpfRne"] == repository._confirmedUsers[0].cpfRne
        assert res.body[id2]["cpfRne"] == repository._confirmedUsers[1].cpfRne
        assert res.body[id3] == {"error": "User not found"}
