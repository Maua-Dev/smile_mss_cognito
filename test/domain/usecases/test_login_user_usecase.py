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
