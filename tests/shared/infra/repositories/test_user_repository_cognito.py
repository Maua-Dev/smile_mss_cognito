import pytest

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.user_repository_cognito import UserRepositoryCognito


class Test_UserRepositoryCognito:

    @pytest.mark.skip("Can't test it locally")
    def test_create_user(self):
        repo = UserRepositoryCognito()
        user_to_create = User(user_id='0000-0000-00000-000000-0000000-00000', email='vgsoller1@gmail.com',
                              name='Doroth Helena de Souza Alves', password="GarrafaDeAguá@#123",
                              ra=None, role=ROLE.EXTERNAL, access_level=ACCESS_LEVEL.USER, created_at=None,
                              updated_at=None, social_name=None, accepted_terms=True,
                              accepted_notifications=True, certificate_with_social_name=False, phone="+5511981643251"
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


