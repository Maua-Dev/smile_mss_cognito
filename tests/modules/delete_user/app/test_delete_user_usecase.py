import pytest

from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, UserNotConfirmed
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="delete_user")

class Test_DeleteUserUsecase:

    def test_delete_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo, observability=observability)

        email = 'zeeba@gmail.com'

        resp = usecase(email)

        assert resp == True

    def test_delete_user_usecase_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo, observability=observability)

        email = 'vilas@gmail.com'

        with pytest.raises(UserNotConfirmed):
            usecase(email)
