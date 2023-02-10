# from datetime import datetime
# import pytest
#
# from src.domain.entities.enums import ROLE, ACCESS_LEVEL
# from src.domain.entities.user import User
# from src.infra.dtos.User.user_dto import CognitoUserDTO
#
#
# class Test_CognitoUserDTO():
#
#     def test_create_valid_user(self):
#         user = User(name='Joao do Teste', cpfRne='93523844070', ra=19003315, role=ROLE.PROFESSOR,
#                     accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
#                     updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@bruno.com',
#                     acceptedTerms=True, acceptedNotifications=True, socialName='Bruno',
#                     certificateWithSocialName=False
#                     )
#
#         userCognitoDto = CognitoUserDTO(user.dict())
#         assert userCognitoDto.name == 'Joao Do Teste'
#         assert userCognitoDto.cpfRne == '93523844070'
#         assert userCognitoDto.role == ROLE.PROFESSOR
#         assert userCognitoDto.accessLevel == ACCESS_LEVEL.ADMIN
#         assert userCognitoDto.ra == '19003315'
#         assert userCognitoDto.password is None
#         assert userCognitoDto.email == 'bruno@bruno.com'
#         assert userCognitoDto.acceptedTerms == True
#         assert userCognitoDto.acceptedNotific == True
#         assert userCognitoDto.socialName == 'Bruno'
#         assert userCognitoDto.certWithSocialName == False
#
#         userAttributes = userCognitoDto.userAttributes
#
#         expectedAttributes = [
#             {'Name': 'name', 'Value': 'Joao Do Teste'},
#             {'Name': 'custom:cpfRne', 'Value': '93523844070'},
#             {'Name': 'custom:ra', 'Value': '19003315'},
#             {'Name': 'email', 'Value': 'bruno@bruno.com'},
#             {'Name': 'custom:accessLevel', 'Value': ACCESS_LEVEL.ADMIN.value},
#             {'Name': 'custom:role', 'Value': ROLE.PROFESSOR.value},
#             {'Name': 'custom:acceptedTerms', 'Value': 'True'},
#             {'Name': 'custom:acceptedNotific', 'Value': 'True'},
#             {'Name': 'custom:socialName', 'Value': 'Bruno'},
#             {'Name': 'custom:certWithSocialName', 'Value': 'False'},
#
#         ]
#
#         for att in expectedAttributes:
#             assert att in userAttributes
#
#
#
#     def test_parse_valid_user(self):
#         user = User(name='Joao do Teste', cpfRne='93523844070', ra=19003315, role=ROLE.PROFESSOR,
#                     accessLevel=ACCESS_LEVEL.ADMIN, email='bruno@bruno.com',
#                     acceptedTerms=True, acceptedNotifications=True, socialName='Bruno',
#                     certificateWithSocialName=False
#                     )
#
#         expectedAttributes = [
#             {'Name': 'name', 'Value': 'Joao Do Teste'},
#             {'Name': 'custom:cpfRne', 'Value': '93523844070'},
#             {'Name': 'custom:ra', 'Value': '19003315'},
#             {'Name': 'email', 'Value': 'bruno@bruno.com'},
#             {'Name': 'custom:accessLevel', 'Value': ACCESS_LEVEL.ADMIN.value},
#             {'Name': 'custom:role', 'Value': ROLE.PROFESSOR.value},
#             {'Name': 'custom:acceptedTerms', 'Value': 'True'},
#             {'Name': 'custom:acceptedNotific', 'Value': 'True'},
#             {'Name': 'custom:socialName', 'Value': 'Bruno'},
#             {'Name': 'custom:certWithSocialName', 'Value': 'False'}
#         ]
#
#         userCognitoDto = CognitoUserDTO.fromKeyValuePair(expectedAttributes)
#         userParsed = userCognitoDto.toEntity()
#         assert user == userParsed
#         assert user.certificateWithSocialName == userParsed.certificateWithSocialName
#         assert user.socialName == userParsed.socialName
#         assert user.acceptedNotifications == userParsed.acceptedNotifications
#
#
#
