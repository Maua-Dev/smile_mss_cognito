from src.modules.list_users.app.list_users_controller import ListUsersController
from src.modules.list_users.app.list_users_usecase import ListUsersUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersController:
    def test_list_users_controller(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        id1 = repo.confirmedUsers[0].user_id
        id2 = repo.confirmedUsers[1].user_id

        user_list = [id1, id2]

        response = controller(HttpRequest(
            body={"user_list": user_list},
            headers={'Authorization': 'Bearer ' + 'validAccessToken-' + repo.confirmedUsers[1].email}))

        assert response.status_code == 200
        assert response.body['user_list'][id1]['user_id'] == id1
        assert response.body['user_list'][id1]['name'] == repo.confirmedUsers[0].name
        assert response.body['user_list'][id1]['email'] == repo.confirmedUsers[0].email
        assert response.body['user_list'][id1]['ra'] == repo.confirmedUsers[0].ra
        assert response.body['user_list'][id1]['role'] == repo.confirmedUsers[0].role.value
        assert response.body['user_list'][id1]['access_level'] == repo.confirmedUsers[0].access_level.value
        assert response.body['user_list'][id1]['social_name'] == repo.confirmedUsers[0].social_name
        assert response.body['user_list'][id2]['user_id'] == id2
        assert response.body['user_list'][id2]['name'] == repo.confirmedUsers[1].name
        assert response.body['user_list'][id2]['email'] == repo.confirmedUsers[1].email
        assert response.body['user_list'][id2]['ra'] == repo.confirmedUsers[1].ra
        assert response.body['user_list'][id2]['role'] == repo.confirmedUsers[1].role.value
        assert response.body['user_list'][id2]['access_level'] == repo.confirmedUsers[1].access_level.value
        assert response.body['user_list'][id2]['social_name'] == repo.confirmedUsers[1].social_name

    def test_list_users_controller_invalid_access_token(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        id1 = repo.confirmedUsers[0].user_id
        id2 = repo.confirmedUsers[1].user_id

        user_list = [id1, id2]

        response = controller(HttpRequest(
            body={"user_list": user_list},
            headers={'Authorization': 'Bearer' + 'validAccessToken-' + repo.confirmedUsers[1].email}))

        assert response.status_code == 400
        assert response.body == 'Field token is not valid'

    def test_list_users_controller_invalid_user_list(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        response = controller(HttpRequest(
            body={"user_list": 1},
            headers={'Authorization': 'Bearer ' + 'validAccessToken-' + repo.confirmedUsers[1].email}))

        assert response.status_code == 400
        assert response.body == 'Field user_list is not valid'

    def test_list_user_controller_missing_authorization(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        id1 = repo.confirmedUsers[0].user_id
        id2 = repo.confirmedUsers[1].user_id

        user_list = [id1, id2]

        response = controller(HttpRequest(
            body={"user_list": user_list}))

        assert response.status_code == 400
        assert response.body == 'Field Authorization header is missing'

    def test_list_user_controller_missing_field_user_list(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        response = controller(HttpRequest(
            body={},
            headers={'Authorization': 'Bearer ' + 'validAccessToken-' + repo.confirmedUsers[1].email}))

        assert response.status_code == 400
        assert response.body == 'Field user_list is missing'

    def test_list_user_controller_access_token_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        id1 = repo.confirmedUsers[0].user_id
        id2 = repo.confirmedUsers[1].user_id

        user_list = [id1, id2]

        response = controller(HttpRequest(
            body={"user_list": user_list},
            headers={'Authorization': 'Bearer ' + 'validAccessToken-' + "notFoundEmail@gmail.com"}))

        assert response.status_code == 404
        assert response.body == 'No items found for user'

    def test_list_user_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        id1 = repo.confirmedUsers[0].user_id
        id2 = repo.confirmedUsers[1].user_id

        user_list = [id1, id2, "1234"]

        response = controller(HttpRequest(
            body={"user_list": user_list},
            headers={'Authorization': 'Bearer ' + 'validAccessToken-' + repo.confirmedUsers[1].email}))

        assert response.status_code == 404
        assert response.body == 'No items found for user_id: 1234'

    def test_list_user_controller_user_id_invalid(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        id1 = repo.confirmedUsers[0].user_id
        id2 = repo.confirmedUsers[1].user_id

        user_list = [id1, id2, "12345"]

        response = controller(HttpRequest(
            body={"user_list": user_list},
            headers={'Authorization': 'Bearer ' + 'validAccessToken-' + repo.confirmedUsers[1].email}))

        assert response.status_code == 400
        assert response.body == 'Field user_id is not valid'

    def test_list_users_controller_forbidden_action(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)
        controller = ListUsersController(usecase)

        id1 = repo.confirmedUsers[0].user_id
        id2 = repo.confirmedUsers[1].user_id

        user_list = [id1, id2]

        response = controller(HttpRequest(
            body={"user_list": user_list},
            headers={'Authorization': 'Bearer ' + 'validAccessToken-' + repo.confirmedUsers[0].email}))

        assert response.status_code == 403
        assert response.body == 'That action is forbidden for this user'






