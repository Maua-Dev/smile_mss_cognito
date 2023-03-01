import datetime

import pytest

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User
from src.shared.infra.repositories.user_repository_cognito import UserRepositoryCognito


class Test_UserRepositoryCognito:

    @pytest.mark.skip("Can't test it locally")
    def test_create_user(self):
        repo = UserRepositoryCognito()
        user_to_create = User(user_id='0000-0000-00000-000000-0000000-00000', email='justdasdacofya@gufum.com',
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

    @pytest.mark.skip("Can't test it locally")
    def test_update_user(self):
        repo = UserRepositoryCognito()
        user_to_update = User(user_id='000000000000000000000000000000000001', email='brunovilardibueno@gmail.com', name='Caio soller', password='z12345',
                 ra='20014309', role=ROLE.INTERNATIONAL_STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                 updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                 accepted_notifications=True, certificate_with_social_name=True, phone="+5511999451100"
                 )
        updated_user = repo.update_user("brunovilardibueno@gmail.com", {'social_name': 'boca roxa', 'certificate_with_social_name': "True"})

        assert True


    @pytest.mark.skip("Can't test it locally")
    def test_delete_user(self):
        repo = UserRepositoryCognito()
        repo.delete_user('21.00208-8@maua.br')

    @pytest.mark.skip("Can't test it locally")
    def test_confirm(self):
        repo = UserRepositoryCognito()
        repo.confirm_user_creation("justacofya@gufum.com", "960499")

    @pytest.mark.skip("Can't test it locally")
    def test_login_user(self):
        repo = UserRepositoryCognito()
        user = repo.login_user("brunovilardibueno@gmail.com", "Teste123!")

        assert user is not None

    @pytest.mark.skip("Can't test it locally")
    def test_check_token(self):
        repo = UserRepositoryCognito()
        repo.check_token("eyJraWQiOiJ4ZmNwemxweXVJajJDOUk5SHdCWXB4bGRSZVZnUjBcL1RyQVNXQUNUSFllQT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJiZGEyNWMwNC00YTY5LTQzYzUtOTAwYy04ODFkMjEyOGE0MTIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0yLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMl91eGJXOU1hQ0wiLCJjbGllbnRfaWQiOiI0OTg1OWttNGlydHJpdHFwOGJqN3A1MnBnbCIsIm9yaWdpbl9qdGkiOiIyNmVjNWVhZS1kNmU0LTQ4YjQtYjgwZC1lZjk0ZDU5ZWY5ZWYiLCJldmVudF9pZCI6IjlkOWJmMzRiLTE0MDUtNDdlYy1hNTc5LTEzYzliZjk2ZTczZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2NzU2MzM2MDgsImV4cCI6MTY3NTYzNzIwOCwiaWF0IjoxNjc1NjMzNjA4LCJqdGkiOiI0MTZmOTMwOC1kMDFlLTQzZjMtYTYwMy1mZjBkY2MxOWZkNmMiLCJ1c2VybmFtZSI6ImJydW5vdmlsYXJkaWJ1ZW5vQGdtYWlsLmNvbSJ9.S9butflLGIvEfgO36RSklWqVS7IBlQLkf5lQhik2ZA8QW0Vzkm8GE3vEjA1TR26y__XPD9UydK2C8x6sKOCkR4uMTiCwTI7rRaC9CYPegibEgU-R3zrgvjjHZPmdVStNxCybViHMUYjzcMVEq0towxYMNLyfjGnDIy551ennMO33oTOfXFRrDmtlGlalVNXNL0qTlY3huubQBhWcARXadSkJ44yKTOzNS__i8qmIIohBfmb2q_YPstnmOOjgVQ3e5Zk73OIjkgsXATWHlM6YUFh-s_oU3zo5e0wfegW7AF_vqe1N6DqnXSLEY4ViShSXzGwSZtNIGqynv69yDQBOMw")

    @pytest.mark.skip("Can't test it locally")
    def test_refresh_token(self):
        repo = UserRepositoryCognito()
        ref = repo.refresh_token("eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.IdOD1Beq5iMlapmR2v3ogaAZQyDrxtgzKDAIA_wz9S6BxY9gb2QxRSQbRJzZz6fyXviCSa5qQR_tBdN97360mQrBMP6Vy9RCUGL5boLyXh9D3Fw6diAUTWCDKWcxYuWFEpx5_CLFxnMiouRCLRLsbQ35dT-Huzanh6psCIDdpMfOlGLhG0exL5ofs3dYF4r9b_tzg9h0PzkmF72q-olbgv-SbQK6Rmp1RYCpPV6p4j1tp8W4H9Fx9Fg7ba4pIxpAgFA9bynRipxzn_NgYQuq7wtAtKLK2oc-mapuq0xAmNnqebzI-UUMAv4dn_AyaYA1HUxxc_JMBwVG5lk_x9a5JA.7wFBbqb_8drKzmw6.gSW9sDTm2KwB1coWzQhiEwYqmmsZEs3YYQDWvPdjlEbqLgZrdDucXpQ2JsfQOIpgnsrjhNoU5lBbc53rr8Hf5OJh2PdBd0l8ZvXJ4zizaaU8gVijadzCPiD3SLRAwa5LLFvY0eh_PVfxCoLqeQplkd9AmEsf_FEB2CDFZRFGB7QWVs2SUNfPSqVl251EBs7HYy2Vf8zVw3JhbnfXqLVTIRRXkbcr_7yMpOKRLLLTL3f635O9xurSi6iIXrxa_2Js7idp-HioJZtIjpJcQG91qiionqcVtJ8youL16kM2KtpnHydaYPxJ1Z98lxQWRfeCAvo7tOPG6w1dTDVVUiFJku0fm-r5oVdl5XnLnX90B9kBMEoc_3aEwPIupkiVQ-RQg_D8nbJiVb24rIifVF9SSPxtr2bJqkxuvoWIE9dqLxXbBQa7fpxsL0rrzHE9do5TAREUJhLHSdsqV9pEUVIQWdCuyN7xDu5IWIC1YHK45n_MfkzDgGMdU5Pd5QqE_KFZL6vjO8CIzUW8hOwcbHvbSRUCGsxbIeBmrw8_hn0EM5LcLmQgL1bXPaz35iFvLNNNSfXHL6EVsi-8DGTKBKYLX9QsjG1oWJsjMKud_smMssIM-GyIgWbfI88TgkuDGfWZY-3w1ZADDDduXVIrJ1xslKQVfUTH_h4bzxgdd7R51hKe7JQOyaLUhK_6IN_cDOn_wOb0B6kJkLRM1MPsfTD0FIsPJb9Nx1V2Y-0yhiECO48-dEc7Mr5A9Ziprgcs7qB7Qoqyk7IF_RhYGoSI2QxR-mhLwJY4vSVtzKw-uPn8gkLNAtbLojXDuG0z2fCjfBrRQ8h6nU5XH8057I96ykq2_wEoZnD723pw3CdU7I94OFIDz3MmkLIuq9xdWv4z9fi4Y2oxQ0iBnstx5zFyGemysyz8pgcgC5gkzA9E8agy6Cmwo_aSrojk-_x2CKRJUIfn7aRwVTKysjMuNPnrWiJAr2yEBfsaou2g_eU555vjTluaOwOiXSVV0hjRZkwWFkAXiamLMN46QT6MbQ2-R_n-BqYLQSMGNGAHvkOIi4hWhWOi3QWnx5GndzB-X2HJ0XwQl2CUEcLndgctA-_YzLTVC_15w1HNmt6abwWyrJMC9vtzm6CsLHSgJ9fvvSGWCx4aXs9j5C0rzMBhX9MTLzAsq8B5WMkOANXsO_pyBcN0IyGWabJ7XLgQg5y4ONSlyihNRr71CSpOt-b1UvjcQp5ZhuxRsLGerbJ8WiXLeASzWWIc2eNFnNhe2NS2ewCbrlvAriXykgL-Xtvh_6miKvwwcgHukavzvWWyt9BFAi7Jeg.ZqrUZ3LALrSVZwZgPQ98kQ")
        assert True

    @pytest.mark.skip("Can't test it locally")
    def test_change_password(self):
        repo = UserRepositoryCognito()
        resp = repo.change_password("brunovilardibueno@gmail.com")
        assert True

    @pytest.mark.skip("Can't test it locally")
    def test_confirm_forgot_password(self):
        repo = UserRepositoryCognito()
        resp = repo.confirm_change_password("brunovilardibueno@gmail.com", "Teste123!", "568273")
        assert True

    @pytest.mark.skip("Can't test it locally")
    def test_resend_confirmation_code(self):
           repo = UserRepositoryCognito()
           resp = repo.resend_confirmation_code("justacofya@gufum.com")
           assert True

    @pytest.mark.skip("Can't test it locally")
    def test_get_all_users(self):
        repo = UserRepositoryCognito()
        resp = repo.get_all_users()
        assert all([isinstance(user, User) for user in resp])

    @pytest.mark.skip("Can't test it locally")
    def test_list_professors(self):
        repo = UserRepositoryCognito()
        resp = repo.list_professors()
        assert all([isinstance(user, User) for user in resp])
        assert all([user.role == ROLE.PROFESSOR for user in resp])

    @pytest.mark.skip("Can't test it locally")
    def test_force_verify_phone_number(self):
        repo = UserRepositoryCognito()
        resp = repo.force_verify_user_phone_number(email="brunovilardibueno@gmail.com")
        assert True
