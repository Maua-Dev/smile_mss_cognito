from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.errors.errors import NoItemsFound, NonExistentUser
from src.domain.usecases.create_user_usecase import CreateUserUsecase
from src.domain.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_CreateUserUsecase:

    @pytest.mark.asyncio
    async def test_create_valid_user(self):
        newUser = User(name='Joana da Testa', cpfRne=12345678914, ra=20004239, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 20, 23, 15), email='joana@testa.com'
                )

        repository = UserRepositoryMock()

        # confirm user does not exist yet
        getUserByCpfRne = GetUserByCpfRneUsecase(repository)
        with pytest.raises(NonExistentUser):
            await getUserByCpfRne(12345678914)


        # create user
        createUserUsecase = CreateUserUsecase(repository)
        await createUserUsecase(newUser)

        # confirm user exists
        createdUser = await getUserByCpfRne(12345678914)
        assert createdUser is not None

        assert createdUser.name == 'Joana Da Testa'
        assert createdUser.cpfRne == 12345678914
        assert createdUser.ra == 20004239
        assert createdUser.role == ROLE.PROFESSOR
        assert createdUser.accessLevel == ACCESS_LEVEL.ADMIN
        assert createdUser.createdAt == datetime(2022, 2, 15, 23, 15)
        assert createdUser.updatedAt == datetime(2022, 2, 20, 23, 15)
        assert createdUser.email == 'joana@testa.com'

