# import pytest
#
# from src.modules.delete_user.app.delete_user_controller import DeleteUserController
# from src.adapters.helpers.http_models import HttpRequest
# from src.domain.errors.errors import NonExistentUser
# from src.modules.get_user.app.get_user_usecase import GetUserByCpfRneUsecase
# from src.infra.repositories.user_repository_mock import UserRepositoryMock
#
#
# class Test_DeleteUserUsecase:
#
#     @pytest.mark.asyncio
#     async def test_delete_valid_user(self):
#         repository = UserRepositoryMock()
#
#         req1 = HttpRequest(body={"cpfRne": repository._users[0].cpfRne})
#         req2 = HttpRequest(body={"cpfRne": repository._users[1].cpfRne})
#
#         deleteUserController = DeleteUserController(repository)
#         res1 = await deleteUserController(req1)
#         res2 = await deleteUserController(req2)
#
#         assert res1.status_code == 200
#         assert res2.status_code == 200
#
#     @pytest.mark.asyncio
#     async def test_delete_non_existent_user(self):
#         repository = UserRepositoryMock()
#
#         req1 = HttpRequest(body={"cpfRne": repository._users[0].cpfRne})
#
#         deleteUserController = DeleteUserController(repository)
#         res1 = await deleteUserController(req1)
#         res2 = await deleteUserController(req1)
#
#         assert res1.status_code == 200
#         assert res2.status_code == 400
#
#     @pytest.mark.asyncio
#     async def test_delete_user_with_invalid_cpf_rne(self):
#         repository = UserRepositoryMock()
#
#         req1 = HttpRequest(body={"cpfRne": "65185"})
#         deleteUserController = DeleteUserController(repository)
#         res1 = await deleteUserController(req1)
#         assert res1.status_code == 400
