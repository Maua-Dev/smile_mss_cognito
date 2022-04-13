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
        repo = UserRepositoryMock()
        getUserByCpfRne = GetUserByCpfRneUsecase(repo)
        user = await getUserByCpfRne('75599469093')
        assert user == repo._confirmedUsers[0]

    @pytest.mark.asyncio
    async def test_get_user_by_cpfrne_2(self):
        repo = UserRepositoryMock()
        getUserByCpfRne = GetUserByCpfRneUsecase(repo)
        user = await getUserByCpfRne('64968222041')
        assert user == repo._confirmedUsers[1]

    @pytest.mark.asyncio
    async def test_get_user_by_non_existent_cpfrne(self):
        getUserByCpfRne = GetUserByCpfRneUsecase(UserRepositoryMock())
        with pytest.raises(NonExistentUser):
            await getUserByCpfRne('27550611033')
        with pytest.raises(NonExistentUser):
            await getUserByCpfRne(1248)

