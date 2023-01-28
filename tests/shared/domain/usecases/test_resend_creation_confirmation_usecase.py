# import pytest
#
# from src.domain.errors.errors import NonExistentUser, EntityError
# from src.modules.resend_creation_confirmation.app.resend_creation_confirmation_usecase import ResendCreationConfirmationUsecase
# from src.infra.repositories.user_repository_mock import UserRepositoryMock
#
#
# class Test_ResendUserCreationConfirmationUsecase:
#
#     @pytest.mark.asyncio
#     async def test_resend_valid_user(self):
#
#         repository = UserRepositoryMock()
#
#         cpf_rne = '75599469093'
#
#         resendUserCreationConfirmationUsecase = ResendCreationConfirmationUsecase(
#             repository)
#         result = await resendUserCreationConfirmationUsecase(cpf_rne)
#
#         assert result
#
#     @pytest.mark.asyncio
#     async def test_resend_invalid_cpf(self):
#
#         repository = UserRepositoryMock()
#
#         cpf_rne = '54134054053'
#
#         resendUserCreationConfirmationUsecase = ResendCreationConfirmationUsecase(
#             repository)
#
#         with pytest.raises(EntityError):
#             await resendUserCreationConfirmationUsecase(cpf_rne)
#
#     @pytest.mark.asyncio
#     async def test_resend_nonexistent_user(self):
#
#         repository = UserRepositoryMock()
#
#         cpf_rne = '43289456021'
#
#         resendUserCreationConfirmationUsecase = ResendCreationConfirmationUsecase(
#             repository)
#
#         with pytest.raises(NonExistentUser):
#             await resendUserCreationConfirmationUsecase(cpf_rne)
