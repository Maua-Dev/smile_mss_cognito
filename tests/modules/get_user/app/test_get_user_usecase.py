import pytest

from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetUserUsecase:

    def test_get_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)
        user = usecase('zeeba@gmail.com')

        assert user == repo.confirmedUsers[0]

    def test_get_user_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        with pytest.raises(EntityError):
            user = usecase('emailinvalido')

    def test_get_user_usecase_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo)

        with pytest.raises(NoItemsFound):
            user = usecase('email@naoexiste.com')
