import pytest
from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:

    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        user = repo.get_user_by_email('zeeba@gmail.com')

        assert user.name == 'Caio Soller'
        assert type(user) == User

    def test_get_all_users(self):
        repo = UserRepositoryMock()
        users = repo.get_all_users()

        assert type(users[0]) == User
        assert type(users) == list
        assert users[0].name == 'Caio Soller'
        assert len(users) == 2

    # def test_create_user(self):
    #     repo = UserRepositoryMock()
    #     repo.create_user(user=User(user_id='0004', email='romas@gmail.com', name='Romas briquez', password='r12345',
    #                                ra='20013459', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
    #                                updated_at=16449777000, social_name='Briquez romas', accepted_terms=True,
    #                                accepted_notifications=True, certificate_with_social_name=True
    #                                ))
    #
    #     assert len(repo.users) == 4
        # assert type(user) == User

    # def test_create_user_already_exists(self):
    #     with pytest.raises(UserAlreadyExists):
    #         repo = UserRepositoryMock()
    #         repo.create_user(user=User(user_id='0004', email='zeeba@maua.br', name='Caio soller', password='z12345',
    #                                    ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
    #                                    updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
    #                                    accepted_notifications=True, certificate_with_social_name=True
    #                                    ))

    def test_check_user_by_propriety(self):
        repo = UserRepositoryMock()
        user_exists = repo.check_user_by_propriety('email', 'zeeba@gmail.com')

        assert user_exists == True

    # def test_confirm_user_creation(self):
    #     repo = UserRepositoryMock()
    #     confirmed = repo.confirm_user_creation('joao@gmail.com', 1234567)
    #
    #     assert confirmed == True
    #     assert repo.confirmed_users[2] == repo.users[2]

    # def test_confirm_user_creation_non_existent_user(self):
    #     repo = UserRepositoryMock()
    #     with pytest.raises(NonExistentUser):
    #         confirmed = repo.confirm_user_creation('zé@gmail.com', 1234567)
    #
    # def test_confirm_user_creation_user_already_confirmed(self):
    #     repo = UserRepositoryMock()
    #     with pytest.raises(UserAlreadyConfirmed):
    #         confirmed = repo.confirm_user_creation('zeeba@gmail.com', 1234567)

    def test_update_user(self):
        repo = UserRepositoryMock()
        repo.update_user(User(user_id='0004', email='vitor@maua.br', name='Caio soller toledo', password='z12345',
                              ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                              updated_at=16449778000, social_name='zeeba toledo', accepted_terms=True,
                              accepted_notifications=True, certificate_with_social_name=True, phone='5511991758098'
                              ))

        assert repo.confirmed_users[1].name == 'Caio Soller Toledo'

    def test_update_user_non_exists(self):
        repo = UserRepositoryMock()
        user =  repo.update_user(User(user_id='0004', email='ze@maua.br', name='Caio soller toledo', password='z12345',
                                  ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                                  updated_at=16449778000, social_name='zeeba toledo', accepted_terms=True,
                                  accepted_notifications=True, certificate_with_social_name=True, phone='5511991758098'
                                  ))
        assert user == None

    def test_delete_user(self):
        repo = UserRepositoryMock()

        assert len(repo.confirmed_users) == 2

        repo.delete_user(email='zeeba@gmail.com')

        assert len(repo.confirmed_users) == 1

    # def test_login_user(self):
    #     repo = UserRepositoryMock()
    #     resp = repo.login_user('zeeba@gmail.com', 'z12345')
    #
    #     assert resp == {
    #         'user_id': '0001',
    #         'email': 'zeeba@gmail.com',
    #         'name': 'Caio Soller',
    #         'ra': '20014309',
    #         'role': ROLE.STUDENT,
    #         'access_level': ACCESS_LEVEL.USER,
    #         'created_at': 16449777000,
    #         'updated_at': 16449777000,
    #         'social_name': 'Zeeba Toledo',
    #         'accepted_terms': True,
    #         'accepted_notifications': True,
    #         'certificate_with_social_name': True,
    #         'accessToken': 'valid_access_token-zeeba@gmail.com',
    #         'refresh_token': 'valid_refresh_token-zeeba@gmail.com'
    #     }

    def test_check_token(self):
        repo = UserRepositoryMock()
        resp = repo.check_token(token="validAccessToken-zeeba@gmail.com")
        assert resp == {
            'user_id': '0001',
            'email': 'zeeba@gmail.com',
            'name': 'Caio Soller',
            'ra': '20014309',
            'role': "STUDENT",
            'access_level': "USER",
            'created_at': 16449777000,
            'updated_at': 16449777000,
            'social_name': 'Zeeba Toledo',
            'accepted_terms': True,
            'accepted_notifications': True,
            'certificate_with_social_name': True,
            'phone': '5511999451100'
        }

    def test_refresh_token(self):
        repo = UserRepositoryMock()
        resp = repo.refresh_token(
            refresh_token="valid_refresh_token-zeeba@gmail.com")
        assert resp[0] == 'valid_access_token-zeeba@gmail.com'
        assert resp[1] == 'valid_refresh_token-zeeba@gmail.com'

    def test_change_password(self):
        repo = UserRepositoryMock()
        resp = repo.change_password('zeeba@gmail.com')

        assert resp == True

    def test_confirm_change_password(self):
        repo = UserRepositoryMock()
        resp = repo.confirm_change_password(
            'zeeba@gmail.com',
            'new1234567',
            '123456'
        )
        assert resp
        assert repo.confirmed_users[0].email == 'zeeba@gmail.com'
        assert repo.confirmed_users[0].password == 'new1234567'

    def test_resend_confirmation_code(self):
        repo = UserRepositoryMock()
        resp = repo.resend_confirmation_code('zeeba@gmail.com')
        assert resp

    # def test_resend_confirmation_code_non_existent_user(self):
    #     repo = UserRepositoryMock()
    #     with pytest.raises(NonExistentUser):
    #         resp = repo.resend_confirmation_code('ze@gmail.com')
