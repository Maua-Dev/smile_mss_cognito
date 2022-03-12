from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetAllUsersUsecase:

    @pytest.mark.asyncio
    async def test_get_all_users(self):
        getAllUsersUsecase = GetAllUsersUsecase(UserRepositoryMock())
        users, count = await getAllUsersUsecase()
        assert len(users) > 0
        assert len(users) == 2
        assert count == len(users)
        assert User(name='user1', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email='bruno@bruno.com', password="123456"
                ) in users
        assert User(name='user2', cpfRne=12345678911, ra=20001231, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), password="123456"
             ) in users

