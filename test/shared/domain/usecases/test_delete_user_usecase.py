import pytest

from src.domain.errors.errors import NonExistentUser
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.modules.get_user.app.get_user_usecase import GetUserByCpfRneUsecase
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_DeleteUserUsecase:

    @pytest.mark.asyncio
    async def test_delete_valid_user(self):
        repository = UserRepositoryMock()

        cpf1 = repository._users[0].cpfRne
        cpf2 = repository._users[1].cpfRne

        deleteUserUsecase = DeleteUserUsecase(repository)
        await deleteUserUsecase(cpf1)
        await deleteUserUsecase(cpf2)

        getUserByCpfRneUsecase = GetUserByCpfRneUsecase(repository)
        with pytest.raises(NonExistentUser):
            await getUserByCpfRneUsecase(cpf1)

        with pytest.raises(NonExistentUser):
            await getUserByCpfRneUsecase(cpf2)

    @pytest.mark.asyncio
    async def test_delete_non_existent_user(self):
        repository = UserRepositoryMock()
        deleteUserUsecase = DeleteUserUsecase(repository)
        with pytest.raises(NonExistentUser):
            await deleteUserUsecase(12345678915)
        with pytest.raises(NonExistentUser):
            await deleteUserUsecase(15748)
