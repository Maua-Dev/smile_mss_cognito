from src.modules.confirm_change_password.app.confirm_change_password_controller import ConfirmChangePasswordController
from src.modules.confirm_change_password.app.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="confirm_change_password")

class Test_ConfirmChangePasswordController:

    def test_confirm_change_password_controller(self):
        repo = UserRepositoryMock()
        usecase = ConfirmChangePasswordUsecase(repo, observability=observability)
        controller = ConfirmChangePasswordController(usecase, observability=observability)
        request = HttpRequest(
            body={
                'email': 'zeeba@gmail.com',
                'new_password': 'SENHA_NOVA',
                'confirmation_code': '123456'
            }
        )
        response = controller(request)

        assert response.status_code == 200
        assert response.body == {'result': True, 'message': ''}

    def test_confirm_change_password_controller_user_not_exist(self):
        repo = UserRepositoryMock()
        usecase = ConfirmChangePasswordUsecase(repo, observability=observability)
        controller = ConfirmChangePasswordController(usecase, observability=observability)
        request = HttpRequest(
            body={
                'email': 'zee@gmail.com',
                'new_password': 'SENHA_NOVA',
                'confirmation_code': '123456'
            }
        )
        response = controller(request)

        assert response.status_code == 400
        assert response.body == {
            'result': False, 'message': 'User not found, invalid confirmation code or weak new password.'}

    def test_confirm_change_password_controller_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = ConfirmChangePasswordUsecase(repo, observability=observability)
        controller = ConfirmChangePasswordController(usecase, observability=observability)
        request = HttpRequest(
            body={
                'email': 'email_invalido',
                'new_password': 'SENHA_NOVA',
                'confirmation_code': '123456'
            }
        )
        response = controller(request)

        assert response.status_code == 400
        assert response.body == {
            'result': False, 'message': 'User not found, invalid confirmation code or weak new password.'}

    def test_confirm_change_password_controller_invalid_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmChangePasswordUsecase(repo, observability=observability)
        controller = ConfirmChangePasswordController(usecase, observability=observability)
        request = HttpRequest(
            body={
                'email': 'zeeba@gmail.com',
                'new_password': 'SENHA_NOVA',
                'confirmation_code': 'codigo_errado'
            }
        )
        response = controller(request)

        assert response.status_code == 400
        assert response.body == {
            'result': False, 'message': 'User not found, invalid confirmation code or weak new password.'}
