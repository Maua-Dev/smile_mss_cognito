import pytest
from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase

from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ChangePasswordUsecase:

    def test_change_password_usecase(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo)
        data = usecase(email='zeeba@gmail.com')

        assert data == True

    def test_change_password_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = ChangePasswordUsecase(repo)

        with pytest.raises(EntityError):
            usecase('emailinvalido.com')
