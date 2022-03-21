from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.errors.errors import NoItemsFound, NonExistentUser, InvalidCredentials, InvalidToken
from src.domain.usecases.create_user_usecase import CreateUserUsecase
from src.domain.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.domain.usecases.login_user_usecase import LoginUserUsecase
from src.domain.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_RefreshTokenUsecase:

    @pytest.mark.asyncio
    async def test_refresh_valid_token(self):

        repository = UserRepositoryMock()

        cpf_rne = '75599469093'
        refreshToken = f'validRefreshToken-{cpf_rne}'

        refreshTokenUsecase = RefreshTokenUsecase(repository)
        accessToken, refreshToken = await refreshTokenUsecase(refreshToken)
        expectedAcessToken = 'validAccessToken-' + str(cpf_rne)
        expectedRefreshToken = 'validRefreshToken-' + str(cpf_rne)

        assert accessToken == expectedAcessToken
        assert refreshToken == expectedRefreshToken

    @pytest.mark.asyncio
    async def test_refresh_token_invalid_token(self):


        cpf_rne = '75599469093'
        refreshToken = f'invalidRefreshToken-{cpf_rne}'

        repository = UserRepositoryMock()

        refreshTokenUsecase = RefreshTokenUsecase(repository)
        with pytest.raises(InvalidToken):
            await refreshTokenUsecase(refreshToken)

    @pytest.mark.asyncio
    async def test_refresh_token_invalid_token2(self):

        cpf_rne = '27550611033'
        refreshToken = f'validRefreshToken-{cpf_rne}'

        repository = UserRepositoryMock()

        refreshTokenUsecase = RefreshTokenUsecase(repository)
        with pytest.raises(InvalidToken):
            await refreshTokenUsecase(refreshToken)
