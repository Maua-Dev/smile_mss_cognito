import datetime

import pytest

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.user_repository_cognito import UserRepositoryCognito


class Test_UserRepositoryCognito:

    @pytest.mark.skip("Can't test it locally")
    def test_create_user(self):
        repo = UserRepositoryCognito()
        user_to_create = User(user_id='0000-0000-00000-000000-0000000-00000', email='21.00208-8@maua.br',
                              name='Maria LUiza Vernasqui Vergani', password="Mauá@#123",
                              ra="21002088", role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                              updated_at=None, social_name="Maluzinha avião", accepted_terms=True,
                              accepted_notifications=True, certificate_with_social_name=False, phone="+5511996396072"
                              )

        new_user = repo.create_user(user_to_create)

        assert new_user.email == user_to_create.email
        assert new_user.name == user_to_create.name
        assert new_user.password == user_to_create.password
        assert new_user.ra == user_to_create.ra
        assert new_user.role == user_to_create.role
        assert new_user.access_level == user_to_create.access_level
        assert new_user.created_at == user_to_create.created_at
        assert new_user.updated_at == user_to_create.updated_at
        assert new_user.social_name == user_to_create.social_name
        assert new_user.accepted_terms == user_to_create.accepted_terms
        assert new_user.accepted_notifications == user_to_create.accepted_notifications
        assert new_user.certificate_with_social_name == user_to_create.certificate_with_social_name
        assert new_user.phone == user_to_create.phone

    @pytest.mark.skip("Can't test it locally")
    def test_get_user_by_email(self):
        repo = UserRepositoryCognito()
        user = repo.get_user_by_email('vgsoller1@gmail.com')

        expected_user = User(
            user_id="4356055b-cbc4-47b4-a31d-497f8a280225",
            email="vgsolle1@gmail.com",
            name="Doroth Helena De Souza Alves",
            password=None,
            ra=None,
            role=ROLE.EXTERNAL,
            access_level=ACCESS_LEVEL.USER,
            created_at=int(datetime.datetime(2023, 2, 3, 23, 27, 48, 713000).timestamp() * 1000),
            updated_at=int(datetime.datetime(2023, 2, 3, 23, 27, 48, 713000).timestamp() * 1000),
            social_name=None,
            accepted_terms=True,
            accepted_notifications=True,
            certificate_with_social_name=False,
            phone="+5511981643251"
        )

        assert user == expected_user

    @pytest.mark.skip("Can't test it locally")
    def test_get_user_by_email_none(self):
        repo = UserRepositoryCognito()
        user = repo.get_user_by_email('dummyemail@gmail.com')

        assert user is None


    @pytest.mark.skip("Can't test it locally")
    def test_get_user_unconfirmed(self):
        repo = UserRepositoryCognito()
        user = repo.get_user_by_email('21.00208-8@maua.br')

        assert user is None

    @pytest.mark.skip("Can't test it locally")
    def test_get_all_users(self):
        repo = UserRepositoryCognito()
        users = repo.get_all_users()
        expected_users = [
            User(
                user_id="4356055b-cbc4-47b4-a31d-497f8a280225",
                email="vgsoller1@gmail.com",
                name="Doroth Helena De Souza Alves",
                password=None,
                ra=None,
                role=ROLE.EXTERNAL,
                access_level=ACCESS_LEVEL.USER,
                created_at=int(datetime.datetime(2023, 2, 3, 23, 27, 48, 713000).timestamp() * 1000),
                updated_at=1675521628988,
                social_name=None,
                accepted_terms=True,
                accepted_notifications=True,
                certificate_with_social_name=False,
                phone="+5511981643251"
            ),
            User(user_id="10f58af7-4c7c-47a3-97e3-0ab9295fce35", email='epucci.devmaua@gmail.com',
                 name='Enzo de Britto Pucci', password=None,
                 ra="21020930", role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=1675519954915,
                 updated_at=1675521573182, social_name=None, accepted_terms=True,
                 accepted_notifications=True, certificate_with_social_name=False, phone="+5511981643251"
                 )
        ]

        users.sort(key=lambda x: x.user_id)
        expected_users.sort(key=lambda x: x.user_id)

        assert len(users) == len(expected_users)

        assert users == expected_users


