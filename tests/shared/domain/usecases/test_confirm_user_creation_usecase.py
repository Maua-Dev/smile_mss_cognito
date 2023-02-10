# import pytest
#
# from src.domain.entities.enums import ACCESS_LEVEL
# from src.domain.errors.errors import InvalidToken, NonExistentUser, UserAlreadyConfirmed
# from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase
# from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
# from src.modules.confirm_change_password.app.confirm_change_password_usecase import ConfirmChangePasswordUsecase
# from src.modules.confirm_user_creation.app.confirm_user_creation_usecase import ConfirmUserCreationUsecase
# from src.modules.refresh_token.app.refresh_token_usecase import RefreshTokenUsecase
# from src.infra.repositories.user_repository_mock import UserRepositoryMock
#
#
# class Test_ConfirmChangePasswordUsecase:
#
#     @pytest.mark.asyncio
#     async def test_confirm_valid_user(self):
#
#         repository = UserRepositoryMock()
#
#         cpf_rne = '54134054052'
#         code = "1234567"
#
#         confirmUserCreationUsecase = ConfirmUserCreationUsecase(repository)
#         result = await confirmUserCreationUsecase(login=cpf_rne, code=code)
#
#         assert result
#         u = await repository.getUserByCpfRne(cpf_rne)
#         assert u.name == "User3"
#         assert u in repository._confirmed_users
#
#     @pytest.mark.asyncio
#     async def test_confirm_confirmed_user(self):
#
#         repository = UserRepositoryMock()
#
#         cpf_rne = '75599469093'
#         code = "1234567"
#
#         confirmUserCreationUsecase = ConfirmUserCreationUsecase(repository)
#         with pytest.raises(UserAlreadyConfirmed):
#             await confirmUserCreationUsecase(login=cpf_rne, code=code)
