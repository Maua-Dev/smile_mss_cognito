import pytest

from src.modules.refresh_token.app.refresh_token_usecase import RefreshTokenUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="refresh_token")

class Test_RefreshTokenUsecase:
    def test_refresh_token_usecase(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)

        tokens = usecase('valid_refresh_token-vitor@maua.br')

        expected_refresh_token = "valid_access_token-vitor@maua.br"
        valid_refresh_token = "valid_refresh_token-vitor@maua.br"
        expected_id_token = "valid_id_token-vitor@maua.br"

        assert tokens[0] == expected_refresh_token
        assert tokens[1] == valid_refresh_token
        assert tokens[2] == expected_id_token

    def test_refresh_token_usecase_invalid_refresh_token(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)

        with pytest.raises(ForbiddenAction):
            tokens = usecase('invalid_refresh_token-vitor@maua.br')

    def test_refresh_token_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo, observability=observability)

        with pytest.raises(ForbiddenAction):
            tokens = usecase('valid_refresh_token-vitor@maua')




