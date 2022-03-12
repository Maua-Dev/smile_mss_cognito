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

    # @pytest.mark.skip(reason="Cognito not set up")
    @pytest.mark.asyncio
    async def test_create_valid_user(self):
        user = User(name='Bruno Vilardi', cpfRne=12345678911, ra=19003315, role=ROLE.STUDENT,
                 accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
                 updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
                 password="Teste123!"
             )


        repo = UserRepositoryCognito()
        response = await repo.createUser(user)

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
        user = User(name='Bruno Vilardi', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
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
        cpfRne = 12345678910
        password = "Teste123!"
        repo = UserRepositoryCognito()
        response = await repo.loginUser(cpfRne, password)
        assert response.get('accessToken') is not None

    # @pytest.mark.skip(reason="Cognito not set up")
    @pytest.mark.asyncio
    async def test_check_token(self):
        cpfRne = 12345678910
        token = 'eyJraWQiOiJIWkFcLzVwMEZqcFwvaUJjS3hcL2xjd2VoQmxLeEVVY2FiTzN3UGROM3NGT0VRPSIsImFsZyI6IlJTMjU2In0.eyJvcmlnaW5fanRpIjoiMmFmODI3NzUtYjY1Ny00ODQ1LTgxZTEtZjJhNDMwNGRhZmQ2Iiwic3ViIjoiNGFkOGMwZjYtYWM1Mi00YzYxLWEwY2QtMGYzYzJiYzVhZTJjIiwiZXZlbnRfaWQiOiJmNzQ0NjZkMC1jNjVkLTQwOTAtYTYzMi01M2FiZWVhYTY5ZTEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjQ3MDQ4MjUyLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV96WVAyNFNPOUUiLCJleHAiOjE2NDcwNTE4NTIsImlhdCI6MTY0NzA0ODI1MiwianRpIjoiYWE5MmZhMWUtMjMwMC00ZDhhLTliMTktMGFhNTE1YzQ1YTVlIiwiY2xpZW50X2lkIjoib2o0NjU4dTBjOHV1NW0xODZyNjhnZWl0diIsInVzZXJuYW1lIjoiMTIzNDU2Nzg5MTAifQ.tg2CsEZwGOYQAdYcZtKPdzIPnvfqNYoaTsZ6ylwTs8WPzo1hfe0Gx6yvr64DBlyAoZ917mIFeS6bU0qaGgioDocYP3JSWqo9eOm0U6TKkBcfG1wTaWhlgh-1KLOs-82fWBhpeun7rC6OmRR2Cme6dsATsU8MYa0F9SpQ6u0VLLQ1adELSJYE8XPVGyOgGSRvTvbwk3NF4T8nFN-1teVk1bH6qVqk7-O-CfAXCcrFzlHDJLZS1desS4MY917JhCz0RNQVDECNF9MO37IPEmcAL-Umu5Kc3Sg5Uz_x7zRtLPRCm5DScnnUNS0hk2zYtDY7VDkS14EipMPtHtQy6_5kcg'
        repo = UserRepositoryCognito()
        response = await repo.checkToken(cpfRne, token)
        assert response


