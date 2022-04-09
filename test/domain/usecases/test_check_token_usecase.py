import pytest

from src.domain.entities.enums import ACCESS_LEVEL
from src.domain.errors.errors import InvalidToken
from src.domain.usecases.check_token_usecase import CheckTokenUsecase
from src.domain.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CheckTokenUsecase:

    @pytest.mark.asyncio
    async def test_check_valid_token(self):

        repository = UserRepositoryMock()

        cpf_rne = '75599469093'
        accessToken = f'validAccessToken-{cpf_rne}'

        checkTokenUsecase = CheckTokenUsecase(repository)
        data = await checkTokenUsecase(accessToken)

        assert data['cpfRne'] == cpf_rne
        assert data['name'] == 'User1'
        assert data['email'] == 'bruno@bruno.com'
        assert data['accessLevel'] == ACCESS_LEVEL.USER

    @pytest.mark.asyncio
    async def test_check_token_invalid_token(self):


        cpf_rne = 75599469093
        refreshToken = f'invalidAccessToken-{cpf_rne}'

        repository = UserRepositoryMock()

        checkTokenUsecase = CheckTokenUsecase(repository)
        with pytest.raises(InvalidToken):
            await checkTokenUsecase(refreshToken)

    @pytest.mark.asyncio
    async def test_check_invalid_token2(self):

        cpf_rne = '30238808084'
        refreshToken = f'validAccessToken-{cpf_rne}'

        repository = UserRepositoryMock()

        checkTokenUsecase = CheckTokenUsecase(repository)
        with pytest.raises(InvalidToken):
            await checkTokenUsecase(refreshToken)