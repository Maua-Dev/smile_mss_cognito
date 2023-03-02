import datetime
import json

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.infra.dtos.User.user_cognito_dto import UserCognitoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserCognitoDTO:

    def test_from_entity(self):
        repo = UserRepositoryMock()
        user = User(user_id='000000000000000000000000000000000003', email='joao@gmail.com', name='João toledo',
                    password='z12345',
                    ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                    updated_at=16449777000, social_name=None, accepted_terms=True,
                    accepted_notifications_sms=True, certificate_with_social_name=True, phone="+5511991758098"
                    )

        user_cognito_dto = UserCognitoDTO.from_entity(user)

        user_cognito_dto_expected = UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            password=user.password,
            ra=user.ra,
            role=user.role,
            access_level=user.access_level,
            created_at=user.created_at,
            updated_at=user.updated_at,
            social_name=user.social_name,
            accepted_terms=user.accepted_terms,
            accepted_notifications_sms=user.accepted_notifications_sms,
            certificate_with_social_name=user.certificate_with_social_name,
            phone=user.phone
        )

        assert user_cognito_dto == user_cognito_dto_expected

    def test_from_entity_none(self):
        user = User(user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo',
                    password=None,
                    ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=None,
                    accepted_notifications_sms=None, certificate_with_social_name=None, phone="5511991758098"
                    )
        user_cognito_dto = UserCognitoDTO.from_entity(user)

        user_cognito_dto_expected = UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            password=user.password,
            ra=user.ra,
            role=user.role,
            access_level=user.access_level,
            created_at=user.created_at,
            updated_at=user.updated_at,
            social_name=user.social_name,
            accepted_terms=user.accepted_terms,
            accepted_notifications_sms=user.accepted_notifications_sms,
            certificate_with_social_name=user.certificate_with_social_name,
            phone=user.phone
        )

        assert user_cognito_dto == user_cognito_dto_expected

    def test_to_cognito_attributes(self):
        repo = UserRepositoryMock()
        user = User(user_id='000000000000000000000000000000000003', email='joao@gmail.com', name='João toledo',
                    password='z12345',
                    ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                    updated_at=16449777000, social_name=None, accepted_terms=True,
                    accepted_notifications_sms=True, certificate_with_social_name=True, phone="+5511991758098"
                    )

        user_cognito_dto = UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            password=user.password,
            ra=user.ra,
            role=user.role,
            access_level=user.access_level,
            created_at=user.created_at,
            updated_at=user.updated_at,
            social_name=user.social_name,
            accepted_terms=user.accepted_terms,
            accepted_notifications_sms=user.accepted_notifications_sms,
            certificate_with_social_name=user.certificate_with_social_name,
            phone=user.phone
        )

        cognito_user_data = user_cognito_dto.to_cognito_attributes()

        assert cognito_user_data == [{'Name': 'email', 'Value': 'joao@gmail.com'},
                                     {'Name': 'name', 'Value': 'João Toledo'},
                                     {'Name': 'custom:role', 'Value': 'STUDENT'},
                                     {'Name': 'custom:accessLevel', 'Value': 'USER'},
                                     {'Name': 'custom:ra', 'Value': '20014309'},
                                     {'Name': 'custom:acceptedTerms', 'Value': 'True'},
                                     {'Name': 'custom:acceptedNotific', 'Value': 'True'},
                                     {'Name': 'custom:certWithSocialName', 'Value': 'True'},
                                     {'Name': 'phone_number', 'Value': '+5511991758098'}]

    def test_from_entity_cognito_attributes(self):
        repo = UserRepositoryMock()

        user = repo.users[0]

        user_cognito_dto = UserCognitoDTO.from_entity(user)

        cognito_user_data = user_cognito_dto.to_cognito_attributes()

        expected_user_attributes = [{'Name': 'email', 'Value': 'zeeba@gmail.com'},
                                    {'Name': 'name', 'Value': 'Caio Soller'},
                                    {'Name': 'custom:role', 'Value': 'STUDENT'},
                                    {'Name': 'custom:accessLevel', 'Value': 'USER'},
                                    {'Name': 'custom:ra', 'Value': '20014309'},
                                    {'Name': 'custom:socialName', 'Value': 'Zeeba Toledo'},
                                    {'Name': 'custom:acceptedTerms', 'Value': 'True'},
                                    {'Name': 'custom:acceptedNotific', 'Value': 'True'},
                                    {'Name': 'custom:certWithSocialName', 'Value': 'True'},
                                    {'Name': 'phone_number', 'Value': '5511999451100'}]

        assert cognito_user_data == expected_user_attributes

    def test_from_entity_to_cognito_attributes_none(self):
        repo = UserRepositoryMock()
        user = User(user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo',
                    password=None,
                    ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=None,
                    accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                    )

        user_cognito_dto = UserCognitoDTO.from_entity(user)

        cognito_user_data = user_cognito_dto.to_cognito_attributes()

        expected_user_attributes = [{'Name': 'email', 'Value': 'zeeba@maua.br'},
                                    {'Name': 'name', 'Value': 'Caio Toledo'},
                                    {'Name': 'custom:role', 'Value': 'STUDENT'},
                                    {'Name': 'custom:accessLevel', 'Value': 'USER'},
                                    {'Name': 'phone_number', 'Value': '+5511991758098'}]

        assert cognito_user_data == expected_user_attributes

    def test_from_cognito(self):
        cognito_data = {'Enabled': True,
                        'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
                                                             'content-length': '709',
                                                             'content-type': 'application/x-amz-json-1.1',
                                                             'date': 'Sat, 04 Feb 2023 13:45:05 GMT',
                                                             'x-amzn-requestid': '8b8fba2d-b2c7-4346-a441-e285892af0a3'},
                                             'HTTPStatusCode': 200,
                                             'RequestId': '8b8fba2d-b2c7-4346-a441-e285892af0a3',
                                             'RetryAttempts': 0},
                        'UserAttributes': [{'Name': 'custom:acceptedTerms', 'Value': 'True'},
                                           {'Name': 'sub',
                                            'Value': '4356055b-cbc4-47b4-a31d-497f8a280225'},
                                           {'Name': 'custom:certWithSocialName', 'Value': 'False'},
                                           {'Name': 'email_verified', 'Value': 'false'},
                                           {'Name': 'name', 'Value': 'Doroth Helena De Souza Alves'},
                                           {'Name': 'phone_number_verified', 'Value': 'false'},
                                           {'Name': 'phone_number', 'Value': '+5511981643251'},
                                           {'Name': 'custom:acceptedNotific', 'Value': 'True'},
                                           {'Name': 'custom:role', 'Value': 'EXTERNAL'},
                                           {'Name': 'email', 'Value': 'vgsoller1@gmail.com'},
                                           {'Name': 'custom:accessLevel', 'Value': 'USER'}],
                        'UserCreateDate': datetime.datetime(2023, 2, 3, 23, 27, 48, 713000),
                        'UserLastModifiedDate': datetime.datetime(2023, 2, 3, 23, 27, 48, 713000),
                        'UserStatus': 'UNCONFIRMED',
                        'Username': 'vgsoller1@gmail.com'}
        user_cognito_dto = UserCognitoDTO.from_cognito(cognito_data)

        user_cognito_expected = UserCognitoDTO(
            user_id='4356055b-cbc4-47b4-a31d-497f8a280225',
            created_at=int(datetime.datetime(2023, 2, 3, 23, 27, 48, 713000).timestamp() * 1000),
            updated_at=int(datetime.datetime(2023, 2, 3, 23, 27, 48, 713000).timestamp() * 1000),
            email="vgsoller1@gmail.com",
            name="Doroth Helena De Souza Alves",
            role=ROLE.EXTERNAL,
            access_level=ACCESS_LEVEL.USER,
            ra=None,
            social_name=None,
            accepted_terms=True,
            accepted_notifications_sms=True,
            certificate_with_social_name=False,
            phone="+5511981643251"
        )

        assert user_cognito_dto == user_cognito_expected

    def test_from_cognito_different_response(self):
        cognito_data = {'Attributes': [{'Name': 'sub',
                                        'Value': '10f58af7-4c7c-47a3-97e3-0ab9295fce35'},
                                       {'Name': 'custom:certWithSocialName', 'Value': 'False'},
                                       {'Name': 'email_verified', 'Value': 'false'},
                                       {'Name': 'phone_number_verified', 'Value': 'false'},
                                       {'Name': 'custom:accessLevel', 'Value': 'USER'},
                                       {'Name': 'custom:acceptedTerms', 'Value': 'True'},
                                       {'Name': 'custom:ra', 'Value': '21020930'},
                                       {'Name': 'name', 'Value': 'Enzo De Britto Pucci'},
                                       {'Name': 'phone_number', 'Value': '+5511981643251'},
                                       {'Name': 'custom:acceptedNotific', 'Value': 'True'},
                                       {'Name': 'custom:role', 'Value': 'STUDENT'},
                                       {'Name': 'email', 'Value': 'epucci.devmaua@gmail.com'}],
                        'Enabled': True,
                        'UserCreateDate': datetime.datetime(2023, 2, 4, 11, 12, 34, 915000),
                        'UserLastModifiedDate': datetime.datetime(2023, 2, 4, 11, 12, 34, 915000),
                        'UserStatus': 'UNCONFIRMED',
                        'Username': 'epucci.devmaua@gmail.com'}

        user_cognito_dto = UserCognitoDTO.from_cognito(cognito_data)

        user_cognito_expected = UserCognitoDTO(
            user_id='10f58af7-4c7c-47a3-97e3-0ab9295fce35',
            created_at=int(datetime.datetime(2023, 2, 4, 11, 12, 34, 915000).timestamp() * 1000),
            updated_at=int(datetime.datetime(2023, 2, 4, 11, 12, 34, 915000).timestamp() * 1000),
            email="epucci.devmaua@gmail.com",
            name="Enzo De Britto Pucci",
            role=ROLE.STUDENT,
            access_level=ACCESS_LEVEL.USER,
            ra="21020930",
            social_name=None,
            accepted_terms=True,
            accepted_notifications_sms=True,
            certificate_with_social_name=False,
            phone="+5511981643251"
        )

        assert user_cognito_dto == user_cognito_expected

    def test_from_cognito_to_entity(self):
        cognito_data = {'Attributes': [{'Name': 'sub',
                                        'Value': '10f58af7-4c7c-47a3-97e3-0ab9295fce35'},
                                       {'Name': 'custom:certWithSocialName', 'Value': 'False'},
                                       {'Name': 'email_verified', 'Value': 'false'},
                                       {'Name': 'phone_number_verified', 'Value': 'false'},
                                       {'Name': 'custom:accessLevel', 'Value': 'USER'},
                                       {'Name': 'custom:acceptedTerms', 'Value': 'True'},
                                       {'Name': 'custom:ra', 'Value': '21020930'},
                                       {'Name': 'name', 'Value': 'Enzo De Britto Pucci'},
                                       {'Name': 'phone_number', 'Value': '+5511981643251'},
                                       {'Name': 'custom:acceptedNotific', 'Value': 'True'},
                                       {'Name': 'custom:role', 'Value': 'STUDENT'},
                                       {'Name': 'email', 'Value': 'epucci.devmaua@gmail.com'}],
                        'Enabled': True,
                        'UserCreateDate': datetime.datetime(2023, 2, 4, 11, 12, 34, 915000),
                        'UserLastModifiedDate': datetime.datetime(2023, 2, 4, 11, 12, 34, 915000),
                        'UserStatus': 'UNCONFIRMED',
                        'Username': 'epucci.devmaua@gmail.com'}

        user_cognito_dto = UserCognitoDTO.from_cognito(cognito_data)

        user_entity = user_cognito_dto.to_entity()

        user_entity_expected = User(user_id="10f58af7-4c7c-47a3-97e3-0ab9295fce35", email='epucci.devmaua@gmail.com',
                 name='Enzo de Britto Pucci', password="GarrafaDeAguá@#123",
                 ra="21020930", role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=None, social_name=None, accepted_terms=True,
                 accepted_notifications_sms=True, certificate_with_social_name=False, phone="+5511981643251"
                 )

        assert user_entity == user_entity_expected
