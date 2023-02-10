# import os
# from datetime import datetime
#
# import pytest
#
# from src.domain.entities.enums import ROLE, ACCESS_LEVEL
# from src.domain.entities.user import User
# from src.domain.errors.errors import NonExistentUser
# from src.infra.dtos.User.user_dto import CognitoUserDTO
# from src.infra.repositories.cognito_repository import UserRepositoryCognito
#
#
# class Test_CognitoRepository():
#
#     # {'ResponseMetadata': {'RequestId': 'ac0e0475-7807-4ff9-a40a-9a70ea606b34', 'HTTPStatusCode': 200,
#     #                       'HTTPHeaders': {'date': 'Fri, 11 Mar 2022 01:33:52 GMT',
#     #                                       'content-type': 'application/x-amz-json-1.1', 'content-length': '2',
#     #                                       'connection': 'keep-alive',
#     #                                       'x-amzn-requestid': 'ac0e0475-7807-4ff9-a40a-9a70ea606b34'},
#     #                       'RetryAttempts': 0}}
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_create_valid_user(self):
#         user = User(name='Bruno Vilardi', cpfRne=12345678919, ra=19003315, role=ROLE.STUDENT,
#                  accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
#                  updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
#                  password="Teste123!"
#              )
#
#
#         repo = UserRepositoryCognito()
#         await repo.createUser(user)
#         # await repo.confirmUserCreationAdmin(user.cpfRne)
#
#     # @pytest.mark.asyncio
#     @pytest.mark.skip(reason="Cognito not set up")
#     async def test_confirm_creation_valid_user(self):
#         user = User(name='Bruno Vilardi', cpfRne=12345678910, ra=19003315, role=ROLE.STUDENT,
#                  accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
#                  updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
#                  password="Teste123!"
#              )
#         user_dto = CognitoUserDTO(user.dict())
#
#         repo = UserRepositoryCognito()
#         response = await repo.confirmUserCreation(user_dto, "284208")
#
#     # @pytest.mark.asyncio
#     @pytest.mark.skip(reason="Cognito not set up")
#     async def test_get_all_user(self):
#         repo = UserRepositoryCognito()
#         response, numberUsers = await repo.getAllUsers()
#         userCognito = response[0]
#         user = User(name='Bruno Vilardi', cpfRne=12345678919, ra=19003315, role=ROLE.STUDENT,
#                  accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
#                  updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
#                  password="Teste123!"
#              )
#         user_dto = CognitoUserDTO(user.dict())
#         assert user_dto.name == userCognito.name
#         assert user_dto.cpfRne == userCognito.cpfRne
#         assert user_dto.ra == userCognito.ra
#         assert user_dto.role == userCognito.role
#         assert user_dto.accessLevel == userCognito.accessLevel
#         assert user_dto.email == userCognito.email
#
#
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_login_user(self):
#         try:
#             cpfRne = 12345678919
#             password = "Teste123!dfasdasd"
#             repo = UserRepositoryCognito()
#             response = await repo.loginUser(cpfRne, password)
#             assert response is not None
#             assert response.get('accessToken') is not None
#             assert response.get('refreshToken') is not None
#             assert response.get('name') == 'Bruno Vilardi'
#             assert response.get('cpfRne') == cpfRne
#         except NonExistentUser as e:
#             assert e
#         except Exception as e:
#             assert e
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_get_user_by_cpfrne(self):
#         cpfRne = 12345678910
#         repo = UserRepositoryCognito()
#         response = await repo.getUserByCpfRne(cpfRne)
#         print(response)
#         assert response.email == 'brunovilardibueno@gmail.com'
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_get_refresh_token(self):
#         cpfRne = 12345678919
#         repo = UserRepositoryCognito()
#         accessToken, refreshToken = await repo.loginUser(cpfRne, "Teste123!")
#         tokens = await repo.refreshToken(refreshToken)
#         accessTokenRefresh, refreshTokenRefresh = tokens
#         assert accessTokenRefresh is not None
#         assert refreshTokenRefresh == refreshToken
#
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_check_token(self):
#         accessToken = "eyJraWQiOiJHbW1ESWNlTjhCakhPWXorNDgxUG9nUzN2NUU4QjY3SkN3eUNsOSsxV1FRPSIsImFsZyI6IlJTMjU2In0.eyJvcmlnaW5fanRpIjoiNmZmMjU1OTYtYmI1Mi00YWNiLTk5NDYtZmMxNTc3ODQwZjlkIiwic3ViIjoiMzA4YzE5NTgtZDQ4MC00OGNlLTg0NjctOGUzMjlhODc0NWUxIiwiZXZlbnRfaWQiOiJiOTlkN2YyNi1lZGQwLTRiMjMtOTYyOC04MTMyMjkyNjQwMTgiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjQ3MjE2NTAzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuc2EtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3NhLWVhc3QtMV9OWTZJZlpicEIiLCJleHAiOjE2NDczMDI5MDMsImlhdCI6MTY0NzIxNjUwMywianRpIjoiMThlMGI5MjAtMjYwZi00MjI5LWE4ZDEtMjEzMjZiYWI2YjRlIiwiY2xpZW50X2lkIjoiMXVya2lnbnJtM2c5ZzE4c2M1NnVhbDgyaHAiLCJ1c2VybmFtZSI6IjEyMzQ5Njk0ODg5In0.qWN6vxhoTRv__0MAwNgHbpX5AgsRCfK91rKqjGKlxRO5w89SX5ulO4b9iFMfQhSkSYSNMkoIcwQBSES7em8e7uvUmt00eRAW5xkx6E3YTtLYKZgvcFkv88TmWQm21S842gypOOFq6GA-b_NnLJEknyedX-6jdta3SdNhUD1tE2P71CY8JDjwSF-YGq-Ean1sGirEbFk1YcS7RN6V7VxrHe9F6xalHoZtl_QeF7-MVaqT_u0Ee9oPprVyQUmMAhBAJ2X72uzyb8Bac03wRRlIUbL6dkj6zUHEapLT087mX7mxG4NG3_fnNCgyMWiMTJNSWEMpCVP2uTsIR8Dfo8OgnQ"
#         repo = UserRepositoryCognito()
#         response = await repo.checkToken(accessToken)
#         assert response is not None
#
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_change_password(self):
#         cpf = 22752461350
#         repo = UserRepositoryCognito()
#         response = await repo.changePassword(str(cpf))
#         assert response is not None
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_confirm_change_password(self):
#         cpf = 22752461350
#         code = 811937
#
#         repo = UserRepositoryCognito()
#         response = await repo.confirmChangePassword(login=str(cpf), newPassword="Teste123!", code=str(code))
#         assert response
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_user_exists(self):
#         user = User(name='Bruno Vilardi', cpfRne=35578159001, ra=19005434, role=ROLE.STUDENT,
#                  accessLevel=ACCESS_LEVEL.USER, createdAt=datetime(2022, 3, 8, 22, 10),
#                  updatedAt=datetime(2022, 3, 8, 22, 15), email="brunovilardibueno@gmail.com",
#                  password="Teste123!"
#              )
#
#         repo = UserRepositoryCognito()
#         response = await repo._checkIfUserExists(user)
#         assert response
#
#     @pytest.mark.skip(reason="Cognito not set up")
#     # @pytest.mark.asyncio
#     async def test_get_all(self):
#         repo = UserRepositoryCognito()
#         response = await repo.getAllUsers()
#         assert response is not None
#
#
#
#
#
#
#
