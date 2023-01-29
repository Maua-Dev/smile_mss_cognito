import pytest

from src.modules.list_users.app.list_users_usecase import ListUsersUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersUsecase:

    def test_list_users_usecase(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        id1 = repo.confirmed_users[0].user_id
        id2 = repo.confirmed_users[1].user_id

        user_list = [id1, id2]

        user_dict = usecase(user_list, "validAccessToken-vitor@maua.br")

        assert len(user_dict) == 2
        assert user_dict[id1] == repo.confirmed_users[0]
        assert user_dict[id2] == repo.confirmed_users[1]

    def test_list_user_usecase_not_found(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        id1 = repo.confirmed_users[0].user_id
        id2 = repo.confirmed_users[1].user_id

        user_list = [id1, id2, "0004"]

        with pytest.raises(NoItemsFound):
            user_dict = usecase(user_list, "validAccessToken-vitor@maua.br")

    def test_list_user_usecase_access_token_not_found(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        id1 = repo.confirmed_users[0].user_id
        id2 = repo.confirmed_users[1].user_id

        user_list = [id1, id2]

        with pytest.raises(NoItemsFound):
            user_dict = usecase(user_list, "validAccessToken-emailfalso@maua.br")

    def test_list_user_usecase_access_token_not_admin(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        id1 = repo.confirmed_users[0].user_id
        id2 = repo.confirmed_users[1].user_id

        user_list = [id1, id2]

        with pytest.raises(NoItemsFound):
            user_dict = usecase(user_list, "validAccessToken-zeeba@gmail.br")

    def test_list_user_usecase_user_list_not_list(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        id1 = repo.confirmed_users[0].user_id
        id2 = repo.confirmed_users[1].user_id

        user_list = id1

        with pytest.raises(EntityError):
            user_dict = usecase(user_list, "validAccessToken-vitor@maua.br")

    def test_list_user_usecase_id_not_valid(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        id1 = repo.confirmed_users[0].user_id
        id2 = repo.confirmed_users[1].user_id

        user_list = [id1, id2, "1"]

        with pytest.raises(EntityError):
            user_dict = usecase(user_list,  "validAccessToken-vitor@maua.br")


