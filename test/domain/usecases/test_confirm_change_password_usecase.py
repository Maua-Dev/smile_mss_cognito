import pytest

from src.domain.entities.enums import ACCESS_LEVEL
from src.domain.errors.errors import InvalidToken
from src.domain.usecases.change_password_usecase import ChangePasswordUsecase
from src.domain.usecases.check_token_usecase import CheckTokenUsecase
from src.domain.usecases.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.domain.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ConfirmChangePasswordUsecase:

    @pytest.mark.asyncio
    async def test_change_valid_user(self):

        repository = UserRepositoryMock()

        cpf_rne = '75599469093'
        code = "123456"

        confirmChangePasswordUsecase = ConfirmChangePasswordUsecase(repository)
        result = await confirmChangePasswordUsecase(login=cpf_rne, newPassword="teste!!!", code=code)

        assert result
        u = await repository.getUserByCpfRne(cpf_rne)
        assert u.password == "teste!!!"

    @pytest.mark.asyncio
    async def test_change_valid_user_email(self):

        repository = UserRepositoryMock()

        email = "user2@user.com"
        code = "123456"

        confirmChangePasswordUsecase = ConfirmChangePasswordUsecase(repository)
        result = await confirmChangePasswordUsecase(login=email, newPassword="teste!!!", code=code)

        assert result
        u = await repository.getUserByCpfRne('64968222041')
        assert u.password == "teste!!!"


    @pytest.mark.asyncio
    async def test_change_non_existent_user(self):
        repository = UserRepositoryMock()

        email = "user2@user.com"
        code = "123456789"

        confirmChangePasswordUsecase = ConfirmChangePasswordUsecase(repository)
        result = await confirmChangePasswordUsecase(login=email, newPassword="teste!!!", code=int(code))

        assert not result
        u = await repository.getUserByCpfRne('64968222041')
        assert u.password != "teste!!!"



    @pytest.mark.asyncio
    async def test_change_invalid_code(self):
        repository = UserRepositoryMock()

        email = "user2@user.com"
        code = "1234567"

        confirmChangePasswordUsecase = ConfirmChangePasswordUsecase(repository)
        result = await confirmChangePasswordUsecase(login=email, newPassword="teste!!!", code=code)

        assert not result
        u = await repository.getUserByCpfRne('64968222041')
        assert u.password != "teste!!!"

    @pytest.mark.asyncio
    async def test_change_non_existent_email(self):

        email = "teste@nada.com"
        code = "123456"

        repository = UserRepositoryMock()

        confirmChangePasswordUsecase = ConfirmChangePasswordUsecase(repository)
        result = await confirmChangePasswordUsecase(login=email, newPassword="teste!!!", code=code)

        assert not result
        u = await repository.getUserByCpfRne('64968222041')
        assert u.password != "teste!!!"