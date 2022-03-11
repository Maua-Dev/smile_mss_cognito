from datetime import datetime

import pytest

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.entities.user import User
from src.infra.dtos.User.user_dto import CognitoUserDTO
from src.infra.repositories.cognito_repository import UserRepositoryCognito


class Test_CognitoRepository():

    # {'ResponseMetadata': {'RequestId': 'ac0e0475-7807-4ff9-a40a-9a70ea606b34', 'HTTPStatusCode': 200,
    #                       'HTTPHeaders': {'date': 'Fri, 11 Mar 2022 01:33:52 GMT',
    #                                       'content-type': 'application/x-amz-json-1.1', 'content-length': '2',
    #                                       'connection': 'keep-alive',
    #                                       'x-amzn-requestid': 'ac0e0475-7807-4ff9-a40a-9a70ea606b34'},
    #                       'RetryAttempts': 0}}

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

    # @pytest.mark.asyncio
    @pytest.mark.skip(reason="Cognito not set up")
    async def test_confirm_creation_valid_user(self):
        user = User(name='Bruno_Vilardi', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
                 password="Teste123!"
             )
        user_dto = CognitoUserDTO(user.dict())

        repo = UserRepositoryCognito()
        response = await repo.confirmUserCreation(user_dto, "317405")

    @pytest.mark.asyncio
    async def test_get_all_user(self):
        repo = UserRepositoryCognito()
        response = repo.getAllUsers()
        userCognito = CognitoUserDTO.fromKeyValuePair(response['Users'][0]['Attributes'])
        print(userCognito)
        user = User(name='Bruno_Vilardi', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
                 password="Teste123!"
             )
        user_dto = CognitoUserDTO(user.dict())
        assert user_dto.name == userCognito.name
        assert user_dto.cpfRne == userCognito.cpfRne
        assert user_dto.ra == userCognito.ra
        assert user_dto.role == userCognito.role
        assert user_dto.accessLevel == userCognito.accessLevel
        assert user_dto.email == userCognito.email

