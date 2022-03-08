import pytest

from src.domain.entities.user import User
from src.domain.errors.errors import NoItemsFound
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetSubjectByCodeUsecase:

    @pytest.mark.asyncio
    async def test_get_user_by_cpfrne_1(self):
        getUserByCpfRne = GetUserByCpfRneUsecase(UserRepositoryMock())
        user = await getUserByCpfRne(12345678910)
        assert user == User(name='user1', cpfRne=12345678910, role='student')

    @pytest.mark.asyncio
    async def test_get_subject_by_code_2(self):
        getUserByCpfRne = GetUserByCpfRneUsecase(UserRepositoryMock())
        user = await getUserByCpfRne(12345678911)
        assert user == User(name='user2', cpfRne=12345678911, role='admin')
