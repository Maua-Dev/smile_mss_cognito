import os
from datetime import datetime

import pytest

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.entities.user import User
from src.infra.dtos.User.user_dto import CognitoUserDTO
from src.infra.repositories.cognito_repository import UserRepositoryCognito


os.environ['AWS_REGION_COGNITO'] = 'sa-east-1'
os.environ['CLIENT_ID'] = '4dk6rsjblaqgojd7p8r3iqqc9t'
os.environ['USER_POOL_ID'] = 'sa-east-1_evH0iIa68'


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
        user = User(name='Bruno Vilardi', cpfRne=12345678919, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
                 password="Teste123!"
             )


        repo = UserRepositoryCognito()
        await repo.createUser(user)
        # await repo.confirmUserCreationAdmin(user.cpfRne)

    # @pytest.mark.asyncio
    @pytest.mark.skip(reason="Cognito not set up")
    async def test_confirm_creation_valid_user(self):
        user = User(name='Bruno Vilardi', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
                 password="Teste123!"
             )
        user_dto = CognitoUserDTO(user.dict())

        repo = UserRepositoryCognito()
        response = await repo.confirmUserCreation(user_dto, "284208")

    # @pytest.mark.asyncio
    @pytest.mark.skip(reason="Cognito not set up")
    async def test_get_all_user(self):
        repo = UserRepositoryCognito()
        response, numberUsers = await repo.getAllUsers()
        userCognito = response[0]
        user = User(name='Bruno Vilardi', cpfRne=12345678919, ra=19003315, role=ROLE.STUDENT,
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



    @pytest.mark.skip(reason="Cognito not set up")
    # @pytest.mark.asyncio
    async def test_login_user(self):
        cpfRne = 12345678919
        password = "Teste123!"
        repo = UserRepositoryCognito()
        response = await repo.loginUser(cpfRne, password)
        assert response is not None
        assert response.get('accessToken') is not None
        assert response.get('refreshToken') is not None
        assert response.get('name') == 'Bruno Vilardi'
        assert response.get('cpfRne') == cpfRne

    @pytest.mark.skip(reason="Cognito not set up")
    # @pytest.mark.asyncio
    async def test_get_user_by_cpfrne(self):
        cpfRne = 12345678910
        repo = UserRepositoryCognito()
        response = await repo.getUserByCpfRne(cpfRne)
        print(response)
        assert response.email == 'brunovilardibueno@gmail.com'

    @pytest.mark.skip(reason="Cognito not set up")
    # @pytest.mark.asyncio
    async def test_get_refresh_token(self):
        cpfRne = 12345678919
        repo = UserRepositoryCognito()
        accessToken, refreshToken = await repo.loginUser(cpfRne, "Teste123!")
        tokens = await repo.refreshToken(refreshToken)
        accessTokenRefresh, refreshTokenRefresh = tokens
        assert accessTokenRefresh is not None
        assert refreshTokenRefresh == refreshToken






