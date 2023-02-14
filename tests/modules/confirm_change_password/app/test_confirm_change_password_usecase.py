import pytest
from src.modules.confirm_change_password.app.confirm_change_password_usecase import ConfirmChangePasswordUsecase

from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ConfirmChangePasswordUsecase:

    def test_confirm_change_password_usecase(self):
        repo = UserRepositoryMock()
        usecase = ConfirmChangePasswordUsecase(repo)
        data = usecase(email='zeeba@gmail.com',
                       new_password='NOVA_SENHA', confirmation_code='123456')

        assert data == True

    def test_confirm_change_password_usecase_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = ConfirmChangePasswordUsecase(repo)
        data = usecase(email='invalid_email.com',
                       new_password='NOVA_SENHA', confirmation_code='123456')
        assert data == False

    def test_confirm_change_password_usecase_invalid_codel(self):
        repo = UserRepositoryMock()
        usecase = ConfirmChangePasswordUsecase(repo)
        data = usecase(email='zeeba@gmail.com',
                       new_password='NOVA_SENHA', confirmation_code='invalid_code')
        assert data == False
