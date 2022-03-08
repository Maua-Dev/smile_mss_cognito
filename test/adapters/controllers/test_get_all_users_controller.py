from src.adapters.controllers.get_all_users_controller import GetAllUsersController
from src.domain.entities.user import User
from src.infra.repositories.user_repository_mock import UserRepositoryMock
from src.adapters.helpers.http_models import HttpRequest, Ok


class Test_GetAllUsersController:

    def test_get_all_users_controller(self):

        getAllUsersController = GetAllUsersController(UserRepositoryMock())
        req = HttpRequest(query=None)
        answer = getAllUsersController(req)

        assert type(answer) == Ok
        assert type(answer.body) is dict
        assert type(answer.body['users']) is list
        assert len(answer.body['users']) == 2
        assert answer.body['count'] == 2
        assert answer.status_code == 200