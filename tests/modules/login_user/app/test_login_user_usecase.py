import pytest

from src.modules.login_user.app.login_user_usecase import LoginUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidCredentials
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_LoginUserUsecase:
    def test_login_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        data = usecase(email="vitor@maua.br", password="z12345")

        assert data["email"] == "vitor@maua.br"
        assert data["access_token"] == "valid_access_token-vitor@maua.br"
        assert data["refresh_token"] == "valid_refresh_token-vitor@maua.br"
        assert data["role"] == "STUDENT"
        assert data["access_level"] == "ADMIN"
        assert 'password' not in data

    def test_login_user_usecase_invalid_password_not_match(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)


        with pytest.raises(InvalidCredentials):
            data = usecase(email="vitor@maua.br", password="invalid_password")

    def test_login_user_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        with pytest.raises(EntityError):
            data = usecase(email="invalid_email", password="z12345")

    def test_login_user_usecase_invalid_password(self):
        repo = UserRepositoryMock()
        usecase = LoginUserUsecase(repo)

        with pytest.raises(EntityError):
            data = usecase(email="vitor@maua.br", password=1)

