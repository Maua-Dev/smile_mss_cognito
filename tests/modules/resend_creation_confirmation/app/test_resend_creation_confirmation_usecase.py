import pytest

from src.modules.resend_creation_confirmation.app.resend_creation_confirmation_usecase import \
    ResendCreationConfirmationUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="resend_creation_confirmation")

class Test_ResendConfirmationUsecase:
    def test_resend_confirmation_usecase(self):
        repo = UserRepositoryMock()
        usecase = ResendCreationConfirmationUsecase(repo, observability=observability)
        result = usecase("vitor@maua.br")

        assert result

    def test_resend_confirmation_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = ResendCreationConfirmationUsecase(repo, observability=observability)

        with pytest.raises(EntityError):
            result = usecase("vitormaua.br")

    def test_resend_confirmation_usecase_nonexistent_email(self):
        repo = UserRepositoryMock()
        usecase = ResendCreationConfirmationUsecase(repo, observability=observability)

        with pytest.raises(NoItemsFound):
            result = usecase("branco@gmail.com")


