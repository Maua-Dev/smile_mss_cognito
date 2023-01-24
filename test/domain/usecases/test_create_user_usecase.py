from datetime import datetime

import pytest

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.domain.errors.errors import NonExistentUser, EntityError
from src.modules.confirm_user_creation.app.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.modules.get_user.app.get_user_usecase import GetUserByCpfRneUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:

    @pytest.mark.asyncio
    async def test_create_valid_user(self):
        newUser = User(name='Joana da Testa', cpfRne='84458081098', ra=20004239, role=ROLE.PROFESSOR,
                       accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(
                           2022, 2, 15, 23, 15),
                       updatedAt=datetime(2022, 2, 20, 23, 15), email='joana@testa.com', password='123456',
                       acceptedTerms=True, acceptedNotifications=True
                       )

        repository = UserRepositoryMock()

        # confirm user does not exist yet
        getUserByCpfRne = GetUserByCpfRneUsecase(repository)
        with pytest.raises(NonExistentUser):
            await getUserByCpfRne('84458081098')

        # create user
        createUserUsecase = CreateUserUsecase(repository)
        await createUserUsecase(newUser)

        # confirm user
        confirmUserUseCase = ConfirmUserCreationUsecase(repository)
        await confirmUserUseCase('84458081098', '1234567')

        # confirm user exists
        createdUser = await getUserByCpfRne('84458081098')
        assert createdUser is not None

        assert createdUser.name == 'Joana Da Testa'
        assert createdUser.cpfRne == '84458081098'
        assert createdUser.ra == '20004239'
        assert createdUser.role == ROLE.PROFESSOR
        assert createdUser.accessLevel == ACCESS_LEVEL.USER
        assert createdUser.createdAt == datetime(2022, 2, 15, 23, 15)
        assert createdUser.updatedAt == datetime(2022, 2, 20, 23, 15)
        assert createdUser.email == 'joana@testa.com'
        assert createdUser.acceptedTerms == True
        assert createdUser.acceptedNotifications == True
        assert createdUser.certificateWithSocialName == False

    @pytest.mark.asyncio
    async def test_create_valid_user_with_social_name(self):
        newUser = User(name='Joana da Testa', cpfRne='84458081098', ra=20004239, role=ROLE.PROFESSOR,
                       accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(
                           2022, 2, 15, 23, 15),
                       updatedAt=datetime(2022, 2, 20, 23, 15), email='joana@testa.com', password='123456',
                       acceptedTerms=True, acceptedNotifications=True, socialName='Joao da Silva'
                       )

        repository = UserRepositoryMock()

        # confirm user does not exist yet
        getUserByCpfRne = GetUserByCpfRneUsecase(repository)
        with pytest.raises(NonExistentUser):
            await getUserByCpfRne('84458081098')

        # create user
        createUserUsecase = CreateUserUsecase(repository)
        await createUserUsecase(newUser)

        # confirm user
        confirmUserUseCase = ConfirmUserCreationUsecase(repository)
        await confirmUserUseCase('84458081098', '1234567')

        # confirm user exists
        createdUser = await getUserByCpfRne('84458081098')
        assert createdUser is not None

        assert createdUser.name == 'Joana Da Testa'
        assert createdUser.cpfRne == '84458081098'
        assert createdUser.ra == '20004239'
        assert createdUser.role == ROLE.PROFESSOR
        assert createdUser.accessLevel == ACCESS_LEVEL.USER
        assert createdUser.createdAt == datetime(2022, 2, 15, 23, 15)
        assert createdUser.updatedAt == datetime(2022, 2, 20, 23, 15)
        assert createdUser.email == 'joana@testa.com'
        assert createdUser.acceptedTerms == True
        assert createdUser.acceptedNotifications == True
        assert createdUser.certificateWithSocialName == True
        assert createdUser.socialName == 'Joao da Silva'

    @pytest.mark.asyncio
    async def test_create_invalid_user(self):
        newUser = User(name='Joana da Testa', cpfRne='84458081098', ra=20004239, role=ROLE.PROFESSOR,
                       accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(
                           2022, 2, 15, 23, 15),
                       updatedAt=datetime(2022, 2, 20, 23, 15), email='joana@testa.com', password='123456',
                       acceptedTerms=True, acceptedNotifications=True
                       )
        repository = UserRepositoryMock()
        createUserUsecase = CreateUserUsecase(repository)

        with pytest.raises(EntityError):
            await createUserUsecase(newUser)
