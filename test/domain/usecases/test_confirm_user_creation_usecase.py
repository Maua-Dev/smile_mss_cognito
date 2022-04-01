import pytest

from src.domain.entities.enums import ACCESS_LEVEL
from src.domain.errors.errors import InvalidToken, NonExistentUser
from src.domain.usecases.change_password_usecase import ChangePasswordUsecase
from src.domain.usecases.check_token_usecase import CheckTokenUsecase
from src.domain.usecases.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.domain.usecases.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.domain.usecases.refresh_token_usecase import RefreshTokenUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ConfirmChangePasswordUsecase:

    @pytest.mark.asyncio
    async def test_change_valid_user(self):

        repository = UserRepositoryMock()

        cpf_rne = '54134054052'
        code = "1234567"

        confirmUserCreationUsecase = ConfirmUserCreationUsecase(repository)
        result = await confirmUserCreationUsecase(login=cpf_rne, code=code)

        assert result
        u = await repository.getUserByCpfRne(cpf_rne)
        assert u.name == "User3"
        assert u in repository._confirmedUsers
