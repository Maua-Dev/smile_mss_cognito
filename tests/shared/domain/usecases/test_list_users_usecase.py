import pytest

from src.modules.list_users.app.list_users_usecase import ListUsersUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUserUsecase:

    @pytest.mark.asyncio
    async def test_list_valid_users(self):
        repository = UserRepositoryMock()

        id1 = repository._users[0].id
        id2 = repository._users[1].id

        l = [id1, id2]
        token = "validAccessToken-64968222041"

        listUsersUsecase = ListUsersUsecase(repository)
        userList = await listUsersUsecase(l, token)

        assert len(userList) == 2
        assert userList[id1] == repository._confirmedUsers[0]
        assert userList[id2] == repository._confirmedUsers[1]

    @pytest.mark.asyncio
    async def test_list_valid_and_non_exitent_users(self):
        repository = UserRepositoryMock()

        id1 = repository._users[0].id
        id2 = repository._users[1].id
        id3 = 57

        l = [id1, id2, id3]
        token = "validAccessToken-64968222041"

        listUsersUsecase = ListUsersUsecase(repository)
        userList = await listUsersUsecase(l, token)

        assert len(userList) == 3
        assert userList[id1] == repository._confirmedUsers[0]
        assert userList[id2] == repository._confirmedUsers[1]
        assert userList[id3] == {"error": "User not found"}
