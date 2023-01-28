# import pytest
#
# from src.modules.login_user.app.login_user_controller import LoginUserController
# from src.modules.refresh_token.app.refresh_token_controller import RefreshTokenController
# from src.modules.update_user.app.update_user_controller import UpdateUserController
# from src.adapters.helpers.http_models import HttpRequest
# from src.domain.entities.enums import ROLE, ACCESS_LEVEL
# from src.infra.repositories.user_repository_mock import UserRepositoryMock
#
#
# class Test_RefreshTokenController:
#
#     @pytest.mark.asyncio
#     async def test_refresh_valid_token_controller(self):
#         header = {"Authorization": "Bearer validRefreshToken-75599469093"}
#         request = HttpRequest(headers=header)
#
#         refreshTokenController = RefreshTokenController(UserRepositoryMock())
#         response = await refreshTokenController(request)
#         assert response.status_code == 200
#         assert response.body == {
#             'access_token': f'validAccessToken-{75599469093}',
#             'refresh_token': f'validRefreshToken-{75599469093}'
#         }
#
#     @pytest.mark.asyncio
#     async def test_login_invalid_token_controller(self):
#         header = {"Authorization": "Bearer invalidRefreshToken-75599469093"}
#         request = HttpRequest(headers=header)
#
#         refreshTokenController = RefreshTokenController(UserRepositoryMock())
#         response = await refreshTokenController(request)
#         assert response.status_code == 400
#
#     @pytest.mark.asyncio
#     async def test_login_non_existent_user_token_controller(self):
#         header = {"Authorization": "Bearer validRefreshToken-19971667045"}
#         request = HttpRequest(headers=header)
#
#         refreshTokenController = RefreshTokenController(UserRepositoryMock())
#         response = await refreshTokenController(request)
#         assert response.status_code == 400
