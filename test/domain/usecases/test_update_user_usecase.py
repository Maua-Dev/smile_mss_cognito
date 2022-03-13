from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.errors.errors import NoItemsFound, UnexpectedError, NonExistentUser
from src.domain.usecases.create_user_usecase import CreateUserUsecase
from src.domain.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.domain.usecases.update_user_usecase import UpdateUserUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_UpdateUserUsecase:

    @pytest.mark.asyncio
    async def test_update_existent_user(self):
        newUser = User(name='user1', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com"
                )

        newUser.name = 'user1_'
        newUser.email = 'user1_@email.com'

        repository = UserRepositoryMock()

        updateUserUsecase = UpdateUserUsecase(repository)
        await updateUserUsecase(newUser)

        # confirm user was updated
        getUserByCpfRneUsecase = GetUserByCpfRneUsecase(repository)
        updatedUser = await getUserByCpfRneUsecase(12345678910)

        assert updatedUser is not None
        assert updatedUser.name == 'user1_'
        assert updatedUser.cpfRne == 12345678910
        assert updatedUser.ra == 19003315
        assert updatedUser.role == ROLE.STUDENT
        assert updatedUser.accessLevel == ACCESS_LEVEL.USER
        assert updatedUser.createdAt == datetime(2022, 3, 8, 22, 10)
        assert updatedUser.updatedAt == datetime(2022, 3, 8, 22, 15)
        assert updatedUser.email == 'user1_@email.com'


    @pytest.mark.asyncio
    async def test_update_existent_user_invalid(self):
        newUser = User(name='user1', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com"
                )
        newUser.cpfRne = 12345678915
        newUser.name = 'user1_'

        repository = UserRepositoryMock()

        updateUserUsecase = UpdateUserUsecase(repository)

        with pytest.raises(NonExistentUser):
            await updateUserUsecase(newUser)

        getUserByCpfRneUsecase = GetUserByCpfRneUsecase(repository)
        userNotUpdated = await getUserByCpfRneUsecase(12345678910)

        assert userNotUpdated.name == 'User1'
        assert userNotUpdated.cpfRne == 12345678910
        assert userNotUpdated.ra == 19003315
        assert userNotUpdated.role == ROLE.STUDENT

    @pytest.mark.asyncio
    async def test_update_existent_user_invalid2(self):
        newUser = User(name='user1', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="bruno@bruno.com"
                )
        newUser.ra = 19003318
        newUser.name = 'user1_'
        newUser.cpfRne = 12345678915

        repository = UserRepositoryMock()

        updateUserUsecase = UpdateUserUsecase(repository)

        with pytest.raises((UnexpectedError, NonExistentUser)):
            await updateUserUsecase(newUser)

        getUserByCpfRneUsecase = GetUserByCpfRneUsecase(repository)
        userNotUpdated = await getUserByCpfRneUsecase(12345678910)

        assert userNotUpdated.name == 'User1'
        assert userNotUpdated.cpfRne == 12345678910
        assert userNotUpdated.ra == 19003315
        assert userNotUpdated.role == ROLE.STUDENT

    @pytest.mark.asyncio
    async def test_update_non_existent_user(self):
        newUser = User(name='Joana da Testa', cpfRne=12345678914, ra=20004239, role=ROLE.PROFESSOR,
                       accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                       updatedAt=datetime(2022, 2, 20, 23, 15), email='joana@testa.com'
                       )
        repository = UserRepositoryMock()
        updateUserUsecase = UpdateUserUsecase(repository)

        with pytest.raises(NonExistentUser):
            await updateUserUsecase(newUser)