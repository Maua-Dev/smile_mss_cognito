from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.errors.errors import NoItemsFound, NonExistentUser
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetUserByCpfRneUsecase:

    @pytest.mark.asyncio
    async def test_get_user_by_cpfrne_1(self):
        getUserByCpfRne = GetUserByCpfRneUsecase(UserRepositoryMock())
        user = await getUserByCpfRne('75599469093')
        assert user == User(name='user1', cpfRne='75599469093', ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email='bruno@bruno.com', password="123456",
                 acceptedTerms=True, acceptedNotifications=False, socialName="Bruno",
                        )

    @pytest.mark.asyncio
    async def test_get_user_by_cpfrne_2(self):
        getUserByCpfRne = GetUserByCpfRneUsecase(UserRepositoryMock())
        user = await getUserByCpfRne('64968222041')
        assert user == User(name='user2', cpfRne='64968222041', ra=20001231, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), password="123456", email="user2@user.com",
                 acceptedTerms=True, acceptedNotifications=True
                        )

    @pytest.mark.asyncio
    async def test_get_user_by_non_existent_cpfrne(self):
        getUserByCpfRne = GetUserByCpfRneUsecase(UserRepositoryMock())
        with pytest.raises(NonExistentUser):
            await getUserByCpfRne('27550611033')
        with pytest.raises(NonExistentUser):
            await getUserByCpfRne(1248)

