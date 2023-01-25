import pytest

from src.modules.resend_creation_confirmation.app.resend_creation_confirmation_controller import ResendCreationConfirmationController
from src.adapters.helpers.http_models import HttpRequest
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ResendCreationConfirmationController:

    @pytest.mark.asyncio
    async def test_resend_valid_cpf(self):
        request = HttpRequest(body={
            'cpf_rne': '75599469093'
        })

        repository = UserRepositoryMock()
        resendCreationConfirmationController = ResendCreationConfirmationController(
            repository)
        response = await resendCreationConfirmationController(request)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_resend_invalid_cpf(self):
        request = HttpRequest(body={
            'cpf_rne': '75599469094'
        })

        repository = UserRepositoryMock()
        resendCreationConfirmationController = ResendCreationConfirmationController(
            repository)
        response = await resendCreationConfirmationController(request)
        assert response.status_code == 400
