from datetime import datetime

import pytest

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.entities.user import User
from src.infra.dtos.User.user_dto import CognitoUserDTO
from src.infra.repositories.cognito_repository import UserRepositoryCognito


class Test_CognitoRepository():

    @pytest.mark.skip(reason="Cognito not set up")
    # @pytest.mark.asyncio
    async def test_create_valid_user(self):
        user = User(name='Bruno_Vilardi', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
                 password="Teste123!"
             )
        user_dto = CognitoUserDTO(user.dict())

        repo = UserRepositoryCognito()
        response = await repo.createUser(user_dto)
        print(response)
        str(response)

