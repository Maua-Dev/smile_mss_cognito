from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserController:
    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        response = controller(HttpRequest(body={'name': 'Vitor', 'social_name': 'Vitinho', 'accepted_notifications_sms': True, 'certificate_with_social_name': True}, headers={'Authorization': 'Bearer ' + 'valid_access_token-' + repo.confirmed_users[0].email}))

        assert response.status_code == 200
        assert response.body['user']['user_id'] == repo.confirmed_users[0].user_id
        assert response.body['user']['name'] == 'Vitor'
        assert response.body['user']['email'] == repo.confirmed_users[0].email
        assert response.body['user']['ra'] == repo.confirmed_users[0].ra
        assert response.body['user']['role'] == repo.confirmed_users[0].role.value
        assert response.body['user']['access_level'] == repo.confirmed_users[0].access_level.value
        assert response.body['user']['social_name'] == 'Vitinho'
        assert eval(response.body['user']['accepted_notifications_sms']) == True
        assert eval(response.body['user']['certificate_with_social_name']) == True
        assert response.body['message'] == 'the user was updated'

    def test_update_user_controller_one_field_only(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        response = controller(HttpRequest(body={'name': 'Vitor'}, headers={'Authorization': 'Bearer ' + 'valid_access_token-' + repo.confirmed_users[0].email}))

        assert response.status_code == 200
        assert response.body['user']['user_id'] == repo.confirmed_users[0].user_id
        assert response.body['user']['name'] == 'Vitor'

    def test_update_user_controller_missing_authorization(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        response = controller(HttpRequest(body={'name': 'Vitor', 'social_name': 'Vitinho', 'accepted_notifications_sms': True, 'certificate_with_social_name': True}))

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: Authorization header'

    def test_update_user_controller_invalid_token(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        response = controller(HttpRequest(
            body={'name': 'Vitor', 'social_name': 'Vitinho', 'accepted_notifications_sms': True,
                  'certificate_with_social_name': True},
            headers={'Authorization': 'Bearer' + 'valid_access_token-' + repo.confirmed_users[0].email}))

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: access_token'

    def test_update_user_controller_no_items_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        response = controller(HttpRequest(body={'name': 'Vitor', 'social_name': 'Vitinho', 'accepted_notifications_sms': True, 'certificate_with_social_name': True}, headers={'Authorization': 'Bearer ' + 'valid_access_token-' + "vitor@vitor.com"}))

        assert response.status_code == 404
        assert response.body == 'Nenhum usuário encontrado'


