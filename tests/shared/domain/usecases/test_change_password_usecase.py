import pytest

from src.domain.entities.enums import ACCESS_LEVEL
from src.domain.errors.errors import InvalidToken
from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase
from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
from src.modules.refresh_token.app.refresh_token_usecase import RefreshTokenUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ChangePasswordUsecase:

    @pytest.mark.asyncio
    async def test_change_valid_user(self):

        repository = UserRepositoryMock()

        cpf_rne = 75599469093

        changePasswordUsecase = ChangePasswordUsecase(repository)
        result = await changePasswordUsecase(str(cpf_rne))

        assert result

    @pytest.mark.asyncio
    async def test_change_valid_user2(self):

        repository = UserRepositoryMock()

        email = "user2@user.com"

        changePasswordUsecase = ChangePasswordUsecase(repository)
        result = await changePasswordUsecase(email)

        assert result

    @pytest.mark.asyncio
    async def test_change_non_existent_cpfRne(self):

        cpf_rne = 71117649008

        repository = UserRepositoryMock()

        changePasswordUsecase = ChangePasswordUsecase(repository)
        result = await changePasswordUsecase(str(cpf_rne))

        assert not result

    @pytest.mark.asyncio
    async def test_change_non_existent_email(self):

        email = "teste@nada.com"

        repository = UserRepositoryMock()

        changePasswordUsecase = ChangePasswordUsecase(repository)
        result = await changePasswordUsecase(email)

        assert not result
