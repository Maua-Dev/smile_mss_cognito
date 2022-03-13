from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.errors.errors import NoItemsFound, NonExistentUser, InvalidCredentials
from src.domain.usecases.create_user_usecase import CreateUserUsecase
from src.domain.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.domain.usecases.login_user_usecase import LoginUserUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_LoginUserUsecase:

    @pytest.mark.asyncio
    async def test_login_valid_user(self):

        cpf_rne = 12345678910
        password = '123456'

        repository = UserRepositoryMock()

        loginUserUsecase = LoginUserUsecase(repository)
        accessToken, refreshToken = await loginUserUsecase(cpf_rne, password)
        expectedAcessToken = 'validAccessToken-' + str(cpf_rne)
        expectedRefreshToken = 'validRefreshToken-' + str(cpf_rne)

        assert accessToken == expectedAcessToken
        assert refreshToken == expectedRefreshToken

    @pytest.mark.asyncio
    async def test_login_invalid_user(self):
        cpf_rne = 12345678910
        password = '1234567'

        repository = UserRepositoryMock()

        loginUserUsecase = LoginUserUsecase(repository)
        with pytest.raises(InvalidCredentials):
            await loginUserUsecase(cpf_rne, password)

    @pytest.mark.asyncio
    async def test_login_non_existent_user(self):
        cpf_rne = 12345678918
        password = '123456'

        repository = UserRepositoryMock()

        loginUserUsecase = LoginUserUsecase(repository)
        with pytest.raises(InvalidCredentials):
            await loginUserUsecase(cpf_rne, password)
