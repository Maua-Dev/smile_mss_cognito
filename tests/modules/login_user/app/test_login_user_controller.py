from src.modules.login_user.app.login_user_controller import LoginUserController
from src.modules.login_user.app.login_user_usecase import LoginUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_LoginUserController:
    def test_login_user_controller(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        controller = LoginUserController(usecase)

        request = HttpRequest(body={
          'login': repo.users[0].email,
          'password': repo.users[0].password
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['user']['access_token'] == f'valid_access_token-{repo.users[0].email}'
        assert response.body['user']['refresh_token'] == f'valid_refresh_token-{repo.users[0].email}'
        assert response.body['user']['id_token'] == f'valid_id_token-{repo.users[0].email}'
        assert response.body['user']['ra'] == repo.users[0].ra
        assert response.body['user']['role'] == repo.users[0].role.value
        assert response.body['user']['access_level'] == repo.users[0].access_level.value
        assert response.body['user']['phone'] == repo.users[0].phone
        assert response.body['user']['email'] == repo.users[0].email
        assert response.body['user']['social_name'] == repo.users[0].social_name
        assert response.body['user']['accepted_notifications_email'] == True
        assert response.body['user']['accepted_notifications_sms'] == True
        assert response.body['user']['name'] == repo.users[0].name
        assert response.body['user']['certificate_with_social_name'] == repo.users[0].certificate_with_social_name
        assert response.body['user']['user_id'] == repo.users[0].user_id
        assert response.body['message'] == 'Login successful'

    def test_login_user_controller_with_missing_login(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        controller = LoginUserController(usecase)

        request = HttpRequest(body={
          'password': repo.users[0].password
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: login'

    def test_login_user_controller_with_missing_password(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        controller = LoginUserController(usecase)

        request = HttpRequest(body={
          'login': repo.users[0].email
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: password'

    def test_login_controller_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        controller = LoginUserController(usecase)

        request = HttpRequest(body={
          'login': 'invalid_email',
          'password': repo.users[0].password
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: email'

    def test_login_controller_invalid_password_not_match(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        controller = LoginUserController(usecase)

        request = HttpRequest(body={
          'login': repo.users[0].email,
          'password': 'invalid_password'
        })

        response = controller(request)

        assert response.status_code == 403
        assert response.body == 'Usuário ou senha inválidos'


    def test_login_controller_invalid_password(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        controller = LoginUserController(usecase)

        request = HttpRequest(body={
          'login': repo.users[0].email,
          'password': 1
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: password'

