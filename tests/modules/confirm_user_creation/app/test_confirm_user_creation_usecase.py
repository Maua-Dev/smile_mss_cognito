import pytest

from src.modules.confirm_user_creation.app.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, UserAlreadyConfirmed, \
    InvalidCredentials, UserNotConfirmed
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ConfirmUserCreationUsecase:

    def test_confirm_user_creation_usecase(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)

        email = 'joao@gmail.com'
        confirmation_code = '102030'

        resp = usecase(email, confirmation_code)

        assert resp == True

    def test_confirm_user_creation_usecase_already_confirmed(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)

        email = 'zeeba@gmail.com'
        confirmation_code = '102030'

        with pytest.raises(UserAlreadyConfirmed):
            usecase(email, confirmation_code)

    def test_confirm_user_creation_usecase_invalid_code(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)

        email = 'joao@gmail.com'
        confirmation_code = '123456'

        with pytest.raises(InvalidCredentials):
            usecase(email, confirmation_code)

    def test_confirm_user_creation_usecase_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = ConfirmUserCreationUsecase(repo)

        email = 'sollito@maua.br'
        confirmation_code = '123456'

        with pytest.raises(NoItemsFound):
            usecase(email, confirmation_code)
