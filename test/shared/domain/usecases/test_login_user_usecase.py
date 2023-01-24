import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.errors.errors import InvalidCredentials
from src.modules.login_user.app.login_user_usecase import LoginUserUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_LoginUserUsecase:

    @pytest.mark.asyncio
    async def test_login_valid_user(self):

        cpf_rne = '75599469093'
        password = '123456'

        repository = UserRepositoryMock()

        loginUserUsecase = LoginUserUsecase(repository)
        data = await loginUserUsecase(cpf_rne, password)
        expectedAcessToken = 'validAccessToken-' + str(cpf_rne)
        expectedRefreshToken = 'validRefreshToken-' + str(cpf_rne)

        assert data["accessToken"] == expectedAcessToken
        assert data["refreshToken"] == expectedRefreshToken
        assert data["cpfRne"] == cpf_rne
        assert data["accessLevel"] == ACCESS_LEVEL.USER
        assert data["role"] == ROLE.STUDENT
        assert data["name"] == 'User1'
        assert data["email"] == 'bruno@bruno.com'

    @pytest.mark.asyncio
    async def test_login_invalid_user(self):
        cpf_rne = '75599469093'
        password = '1234567'

        repository = UserRepositoryMock()

        loginUserUsecase = LoginUserUsecase(repository)
        with pytest.raises(InvalidCredentials):
            await loginUserUsecase(cpf_rne, password)

    @pytest.mark.asyncio
    async def test_login_non_existent_user(self):
        cpf_rne = '27550611033'
        password = '123456'

        repository = UserRepositoryMock()

        loginUserUsecase = LoginUserUsecase(repository)
        with pytest.raises(InvalidCredentials):
            await loginUserUsecase(cpf_rne, password)
