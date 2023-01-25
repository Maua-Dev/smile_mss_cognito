from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.errors.errors import InvalidToken
from src.modules.get_user.app.get_user_usecase import GetUserByCpfRneUsecase
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:

    @pytest.mark.asyncio
    async def test_update_existent_user(self):
        oldUser = User(name='user1', cpfRne='75599469093', ra=19003315, role=ROLE.STUDENT,
                       accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(
                           2022, 3, 8, 22, 10),
                       updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com"
                       )

        newUser = oldUser.copy()
        newUser.name = 'user1_'

        repository = UserRepositoryMock()

        updateUserUsecase = UpdateUserUsecase(repository)
        await updateUserUsecase(newUser.dict(), f"validAccessToken-{oldUser.cpfRne}")

        # confirm user was updated
        getUserByCpfRneUsecase = GetUserByCpfRneUsecase(repository)
        updatedUser = await getUserByCpfRneUsecase('75599469093')

        assert updatedUser is not None
        assert updatedUser.name == 'user1_'
        assert updatedUser.name != oldUser.cpfRne
        assert updatedUser.cpfRne == oldUser.cpfRne
        assert updatedUser.ra == oldUser.ra
        assert updatedUser.role == oldUser.role
        assert updatedUser.accessLevel == oldUser.accessLevel
        assert updatedUser.createdAt == oldUser.createdAt
        assert updatedUser.updatedAt == oldUser.updatedAt
        assert updatedUser.email == oldUser.email

    @pytest.mark.asyncio
    async def test_update_existent_user2(self):
        oldUser = User(name='user1', cpfRne='75599469093', ra=19003315, role=ROLE.STUDENT,
                       accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(
                           2022, 3, 8, 22, 10),
                       updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com"
                       )

        newUser = oldUser.copy()
        newUser.name = 'user2_'
        newUser.socialName = 'userx_'

        repository = UserRepositoryMock()

        updateUserUsecase = UpdateUserUsecase(repository)
        await updateUserUsecase(newUser.dict(), f"validAccessToken-{oldUser.cpfRne}")

        # confirm user was updated
        getUserByCpfRneUsecase = GetUserByCpfRneUsecase(repository)
        updatedUser = await getUserByCpfRneUsecase('75599469093')

        assert updatedUser is not None
        assert updatedUser.name == 'user2_'
        assert updatedUser.name != oldUser.name
        assert updatedUser.socialName == 'userx_'
        assert updatedUser.socialName != oldUser.socialName
        assert updatedUser.cpfRne == oldUser.cpfRne
        assert updatedUser.ra == oldUser.ra
        assert updatedUser.role == oldUser.role
        assert updatedUser.accessLevel == oldUser.accessLevel
        assert updatedUser.createdAt == oldUser.createdAt
        assert updatedUser.updatedAt == oldUser.updatedAt
        assert updatedUser.email == oldUser.email

    @pytest.mark.asyncio
    async def test_update_existent_user_access_level(self):
        oldUser = User(name='user1', cpfRne='75599469093', ra=19003315, role=ROLE.STUDENT,
                       accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(
                           2022, 3, 8, 22, 10),
                       updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com"
                       )
        newUser = oldUser.copy()
        newUser.name = 'user1_'
        newUser.accessLevel = ACCESS_LEVEL.ADMIN

        repository = UserRepositoryMock()

        updateUserUsecase = UpdateUserUsecase(repository)

        await updateUserUsecase(newUser.dict(), f"validAccessToken-{oldUser.cpfRne}")

        getUserByCpfRneUsecase = GetUserByCpfRneUsecase(repository)
        userNotUpdated = await getUserByCpfRneUsecase('75599469093')

        assert userNotUpdated.name == 'user1_'
        assert userNotUpdated.cpfRne == '75599469093'
        assert userNotUpdated.ra == '19003315'
        assert userNotUpdated.role == ROLE.STUDENT
        assert userNotUpdated.accessLevel == ACCESS_LEVEL.USER

    @pytest.mark.asyncio
    async def test_update_non_existent_user(self):
        newUser = User(name='Joana da Testa', cpfRne='27550611033', ra=20004239, role=ROLE.PROFESSOR,
                       accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(
                           2022, 2, 15, 23, 15),
                       updatedAt=datetime(2022, 2, 20, 23, 15), email='joana@testa.com'
                       )
        repository = UserRepositoryMock()
        updateUserUsecase = UpdateUserUsecase(repository)

        with pytest.raises(InvalidToken):
            await updateUserUsecase(newUser.dict(), f"validAccessToken-{newUser.cpfRne}")
