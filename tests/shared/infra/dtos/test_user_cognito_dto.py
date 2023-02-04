import json

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.infra.dtos.User.user_cognito_dto import UserCognitoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserCognitoDTO:

    def test_from_entity(self):
        repo = UserRepositoryMock()
        user = User(user_id='000000000000000000000000000000000003', email='joao@gmail.com', name='João toledo', password='z12345',
                         ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                         updated_at=16449777000, social_name=None, accepted_terms=True,
                         accepted_notifications=True, certificate_with_social_name=True, phone="+5511991758098"
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
            accepted_notifications=user.accepted_notifications,
            certificate_with_social_name=user.certificate_with_social_name,
            phone=user.phone
        )

        assert user_cognito_dto == user_cognito_dto_expected

    def test_from_entity_none(self):
        user = User(user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo',
                    password=None,
                    ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=None,
                    accepted_notifications=None, certificate_with_social_name=None, phone="5511991758098"
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
            accepted_notifications=user.accepted_notifications,
            certificate_with_social_name=user.certificate_with_social_name,
            phone=user.phone
        )

        assert user_cognito_dto == user_cognito_dto_expected

    def test_to_cognito_attributes(self):
        repo = UserRepositoryMock()
        user = User(user_id='000000000000000000000000000000000003', email='joao@gmail.com', name='João toledo', password='z12345',
                         ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                         updated_at=16449777000, social_name=None, accepted_terms=True,
                         accepted_notifications=True, certificate_with_social_name=True, phone="+5511991758098"
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
            accepted_notifications=user.accepted_notifications,
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
                    accepted_notifications=None, certificate_with_social_name=None, phone="+5511991758098"
                    )

        user_cognito_dto = UserCognitoDTO.from_entity(user)

        cognito_user_data = user_cognito_dto.to_cognito_attributes()

        expected_user_attributes = [{'Name': 'email', 'Value': 'zeeba@maua.br'},
                                    {'Name': 'name', 'Value': 'Caio Toledo'},
                                    {'Name': 'custom:role', 'Value': 'STUDENT'},
                                    {'Name': 'custom:accessLevel', 'Value': 'USER'},
                                    {'Name': 'phone_number', 'Value': '+5511991758098'}]

        assert cognito_user_data == expected_user_attributes
