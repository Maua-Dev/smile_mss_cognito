import pytest

from src.domain.entities.user import User
from src.domain.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetAllUsersUsecase:

    def test_get_all_users(self):
        getAllUsersUsecase = GetAllUsersUsecase(UserRepositoryMock())
        users, count = getAllUsersUsecase()
        assert len(users) > 0
        assert len(users) == 2
        assert count == len(users)
        assert User(name='user1', cpfRne=12345678910, role='student') in users
        assert User(name='user2', cpfRne=12345678911, role='admin') in users

