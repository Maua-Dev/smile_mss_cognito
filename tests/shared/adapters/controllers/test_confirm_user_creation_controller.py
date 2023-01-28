# import pytest
#
# from src.modules.change_password.app.change_password_controller import ChangePasswordController
# from src.modules.confirm_change_password.app.confirm_change_password_controller import ConfirmChangePasswordController
# from src.modules.confirm_user_creation.app.confirm_user_creation_controller import ConfirmUserCreationController
# from src.modules.login_user.app.login_user_controller import LoginUserController
# from src.modules.update_user.app.update_user_controller import UpdateUserController
# from src.adapters.helpers.http_models import HttpRequest
# from src.domain.entities.enums import ROLE, ACCESS_LEVEL
# from src.infra.repositories.user_repository_mock import UserRepositoryMock
#
#
# class Test_ConfirmChangePasswordController:
#
#     @pytest.mark.asyncio
#     async def test_confirm_valid_cpfRne_controller(self):
#         request = HttpRequest(body={
#             'login': '54134054052',
#             'code': '1234567'
#         })
#
#         repository = UserRepositoryMock()
#         confirmUserCreationController = ConfirmUserCreationController(
#             repository)
#         response = await confirmUserCreationController(request)
#         assert response.status_code == 200
#         u = await repository.getUserByCpfRne('54134054052')
#         assert u.name == 'User3'
#
#     @pytest.mark.asyncio
#     async def test_confirm_confirmed_user_controller(self):
#         request = HttpRequest(body={
#             'login': '75599469093',
#             'code': '1234567'
#         })
#
#         repository = UserRepositoryMock()
#         confirmUserCreationController = ConfirmUserCreationController(
#             repository)
#         response = await confirmUserCreationController(request)
#         assert response.status_code == 303
#
#     @pytest.mark.asyncio
#     async def test_confirm_unexistent_user_controller(self):
#         request = HttpRequest(body={
#             'login': '12345678910',
#             'code': '1234567'
#         })
#
#         repository = UserRepositoryMock()
#         confirmUserCreationController = ConfirmUserCreationController(
#             repository)
#         response = await confirmUserCreationController(request)
#         assert response.status_code == 404
