from src.modules.get_user.app.get_user_controller import GetUserController
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserController:

    def test_get_user_controller(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)
        controller = GetUserController(usecase)

        response = controller(HttpRequest(query_params={'email': "zeeba@gmail.com"}))

        assert response.status_code == 200
        assert response.body['user']['user_id'] == repo.confirmed_users[0].user_id
        assert response.body['user']['name'] == repo.confirmed_users[0].name
        assert response.body['user']['email'] == repo.confirmed_users[0].email
        assert response.body['user']['ra'] == repo.confirmed_users[0].ra
        assert response.body['user']['role'] == repo.confirmed_users[0].role.value
        assert response.body['user']['access_level'] == repo.confirmed_users[0].access_level.value
        assert response.body['user']['social_name'] == repo.confirmed_users[0].social_name
        assert response.body['message'] == 'the user was retrieved'

    def test_get_user_missing_email(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)
        controller = GetUserController(usecase)

        response = controller(HttpRequest(query_params={}))

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: email'

    def test_get_user_entity_error(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)
        controller = GetUserController(usecase)

        response = controller(HttpRequest(query_params={'email': 'invalid_email'}))

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: email'

    def test_get_user_no_items_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)
        controller = GetUserController(usecase)

        response = controller(HttpRequest(query_params={'email': 'vitor@vitinho.com'}))

        assert response.status_code == 404
        assert response.body == 'Nenhum usuário encontrado'


