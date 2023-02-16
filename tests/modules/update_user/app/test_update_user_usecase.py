import pytest

from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:

    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)

        user_to_update = {
            'email': 'zeeba@gmail.com',
            'name': 'Vitor BARTOLOZZI TOLEDO',
        }

        old_user = repo.confirmed_users[0]
        new_user = usecase(mew_user_data=user_to_update, access_token=f"valid_access_token-{user_to_update['email']}")

        assert new_user.name == "Vitor BARTOLOZZI TOLEDO"
        assert repo.confirmed_users[0].name == "Vitor BARTOLOZZI TOLEDO"
        assert repo.confirmed_users[0].social_name == old_user.social_name
        assert repo.confirmed_users[0].accepted_notifications == old_user.accepted_notifications
        assert repo.confirmed_users[0].certificate_with_social_name == old_user.certificate_with_social_name


    def test_update_user_usecase_more_fields(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)

        user_to_update = {
            'email': 'zeeba@gmail.com',
            'ra': "21014442",
            'name': 'Vitor BARTOLOZZI BASTOS GODOY DE TOLEDO',
            'social_name': 'Vitor Godoy',
            'accepted_notifications': "True",
            'certificate_with_social_name': True,
            'phone': '11999999999'
        }

        old_user = repo.confirmed_users[0]

        new_user = usecase(mew_user_data=user_to_update, access_token=f"valid_access_token-{user_to_update['email']}")

        assert new_user.name == 'Vitor BARTOLOZZI BASTOS GODOY DE TOLEDO'
        assert new_user.social_name == 'Vitor Godoy'
        assert new_user.accepted_notifications
        assert new_user.certificate_with_social_name
        assert repo.confirmed_users[0].name == 'Vitor BARTOLOZZI BASTOS GODOY DE TOLEDO'
        assert repo.confirmed_users[0].social_name == 'Vitor Godoy'
        assert repo.confirmed_users[0].accepted_notifications
        assert repo.confirmed_users[0].certificate_with_social_name
        assert repo.confirmed_users[0].phone == '11999999999'
        assert repo.confirmed_users[0].ra == old_user.ra
        assert repo.confirmed_users[0].accepted_terms == old_user.accepted_terms

    def test_update_user_usecase_invalid_access_token(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)

        user_to_update = {
            'email': 'zeeba@gmail.com',
            'name': 'Vitor BARTOLOZZI BASTOS GODOY DE TOLEDO',
        }

        with pytest.raises(EntityError):
            new_user = usecase(mew_user_data=user_to_update,
                               access_token=f"invalid_access_token-{user_to_update['email']}")

    def test_update_user_usecase_i(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)

        user_to_update = {
            'email': 'vitor@vitor.com',
            'name': 'Vitor BARTOLOZZI BASTOS GODOY DE TOLEDO',
        }

        with pytest.raises(NoItemsFound):
            new_user = usecase(mew_user_data=user_to_update,
                               access_token=f"valid_access_token-{user_to_update['email']}")



