from datetime import datetime

import pytest

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.domain_errors import EntityError


# from src.shared.domain.errors.errors import EntityError


class Test_User:

    def test_create_valid_user_all_fields_completed(self):
        user = User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@gmail.com', name='Caio toledo', password='z12345',
                    ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                    updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                    accepted_notifications_sms=True, certificate_with_social_name=True, phone="+5511991758098"
                    )

        assert len(user.user_id) == 36
        assert user.user_id == '0000-0000-00000-000000-0000000-00000'
        assert user.email == 'zeeba@gmail.com'
        assert len(user.name) > 1
        assert user.name == 'Caio Toledo'
        assert user.password == 'z12345'
        assert user.ra == '20014309'
        assert user.role == ROLE.STUDENT
        assert user.access_level == ACCESS_LEVEL.USER
        assert user.created_at == 16449777000
        assert user.updated_at == 16449777000
        assert user.social_name == 'Zeeba Toledo'
        assert user.accepted_terms == True
        assert user.accepted_notifications_sms == True
        assert user.certificate_with_social_name == True

    def test_create_valid_user_only_required_fields(self):
        user = User(accepted_notifications_email=True, user_id=None, email='zeeba@maua.br', name='caio toledo', password=None,
                    ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=None,
                    accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                    )

        assert user.user_id == None
        assert user.email == 'zeeba@maua.br'
        assert len(user.name) > 1
        assert user.name == 'Caio Toledo'
        assert user.password is None
        assert user.ra is None
        assert user.role == ROLE.STUDENT
        assert user.access_level == ACCESS_LEVEL.USER
        assert user.created_at is None
        assert user.updated_at is None
        assert user.social_name is None
        assert user.accepted_terms is None
        assert user.accepted_notifications_sms is None
        assert user.certificate_with_social_name is None

    def test_create_user_invalid_user_id(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='1234', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )




    def test_create_user_invalid_email(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeebamaua.br', name='caio toledo', password=None,
                 ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_name(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='c', password=None,
                 ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_password(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=1,
                 ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_ra(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_role(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role='STUDENT', access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_access_level(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role=ROLE.STUDENT, access_level='USER', created_at=None,
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_created_at(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at='16449777000',
                 updated_at=None, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_updated_at(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at='16449777000', social_name=None, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_social_name(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                 updated_at=None, social_name=1, accepted_terms=None,
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_accepted_terms(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=16449777000, social_name=None, accepted_terms='True',
                 accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_accepted_notifications_sms(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=16449777000, social_name=None, accepted_terms=None,
                 accepted_notifications_sms='None', certificate_with_social_name=None, phone="+5511991758098"
                 )

    def test_create_user_invalid_certificate_with_social_name(self):
        with pytest.raises(EntityError):
            User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                 ra='12345678', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                 updated_at=16449777000, social_name=None, accepted_terms=None,
                 accepted_notifications_sms=False, certificate_with_social_name='None', phone="+5511991758098"
                 )

    def test_user_to_dict(self):
        user = User(accepted_notifications_email=True, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@gmail.com', name='Caio toledo', password='z12345',
                    ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                    updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                    accepted_notifications_sms=True, certificate_with_social_name=True, phone="+5511991758098"
                    )
        data = User.to_dict(user)

        expected_data = {
            'user_id': '0000-0000-00000-000000-0000000-00000',
            'email': 'zeeba@gmail.com',
            'name': 'Caio Toledo',
            'password': 'z12345',
            'ra': '20014309',
            'role': 'STUDENT',
            'access_level': 'USER',
            'created_at': 16449777000,
            'updated_at': 16449777000,
            'social_name': 'Zeeba Toledo',
            'accepted_terms': True,
            'accepted_notifications_sms': True,
            'accepted_notifications_email': True,
            'certificate_with_social_name': True,
            'phone': '+5511991758098'
        }

        assert data == expected_data

    def test_user_to_dict_none(self):
        user = User(accepted_notifications_email=None, user_id='0000-0000-00000-000000-0000000-00000', email='zeeba@maua.br', name='caio toledo', password=None,
                    ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=None,
                    accepted_notifications_sms=None, certificate_with_social_name=None, phone="+5511991758098"
                    )

        data = User.to_dict(user)

        expected_data = {
            'user_id': '0000-0000-00000-000000-0000000-00000',
            'email': 'zeeba@maua.br',
            'name': 'Caio Toledo',
            'password': None,
            'ra': None,
            'role': 'STUDENT',
            'access_level': 'USER',
            'created_at': None,
            'updated_at': None,
            'social_name': None,
            'accepted_terms': None,
            'accepted_notifications_sms': None,
            'accepted_notifications_email': None,
            'certificate_with_social_name': None,
            'phone': '+5511991758098'
        }

        assert data == expected_data

    def test_user_from_dict(self):
        data = {
            'user_id': '0000-0000-00000-000000-0000000-00000',
            'email': 'vitin@maua.br',
            'name': 'Vitor Toledo',
            'password': 'z12345',
            'ra': '20014309',
            'role': 'STUDENT',
            'access_level': 'USER',
            'created_at': 16449777000,
            'updated_at': 16449777000,
            'social_name': 'Vitor Toledo',
            'accepted_terms': True,
            'accepted_notifications_sms': True,
            'accepted_notifications_email': False,
            'certificate_with_social_name': True,
            'phone': '+5511991758098'
        }

        user = User.parse_object(data)

        assert type(user) == User
        assert user.user_id == '0000-0000-00000-000000-0000000-00000'
        assert user.email == 'vitin@maua.br'
        assert user.name == 'Vitor Toledo'
        assert user.password == 'z12345'
        assert user.ra == '20014309'
        assert user.role == ROLE.STUDENT
        assert user.access_level == ACCESS_LEVEL.USER
        assert user.created_at == 16449777000
        assert user.updated_at == 16449777000
        assert user.social_name == 'Vitor Toledo'
        assert user.accepted_terms == True
        assert user.accepted_notifications_sms == True
        assert user.accepted_notifications_email == False
        assert user.certificate_with_social_name == True
        assert user.phone == '+5511991758098'

    def test_user_from_dict_none(self):
        data = {
            'user_id': None,
            'email': 'vitin@maua.br',
            'name': 'Vitor Toledo',
            'password': None,
            'ra': None,
            'role': 'STUDENT',
            'access_level': 'USER',
            'created_at': None,
            'updated_at': None,
            'social_name': None,
            'accepted_terms': None,
            'accepted_notifications_sms': None,
            'accepted_notifications_email': None,
            'certificate_with_social_name': None,
            'phone': '+5511991758098'
        }

        user = User.parse_object(data)

        assert type(user) == User
        assert user.user_id == None
        assert user.email == 'vitin@maua.br'
        assert user.name == 'Vitor Toledo'
        assert user.password == None
        assert user.ra == None
        assert user.role == ROLE.STUDENT
        assert user.access_level == ACCESS_LEVEL.USER
        assert user.created_at == None
        assert user.updated_at == None
        assert user.social_name == None
        assert user.accepted_terms == None
        assert user.accepted_notifications_sms == None
        assert user.accepted_notifications_email == None
        assert user.certificate_with_social_name == None

    def test_user_professor_maua(self):
        email = "vitor@maua.br"

        assert User.validate_email_maua_professor(email)

    def test_user_professor_maua_invalid(self):
        email = "21.01444-2@maua.br"

        assert not User.validate_email_maua_professor(email)
