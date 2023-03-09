import pytest

from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, DuplicatedItem, TermsNotAcceptedError
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:
    def test_create_user_usecase(self):

        user = User(user_id='000000000000000000000000000000000000', email='vitor@gmail.com', name='Vitor soller', password='z12345',
                    ra=None, role=ROLE.EXTERNAL, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True,
                    accepted_notifications_sms=True, certificate_with_social_name=False, phone="+5511991758098", accepted_notifications_email=True)
        repo = UserRepositoryMock()
        len_before = len(repo.users)
        usecase = CreateUserUsecase(repo)

        new_user = usecase(user)

        assert type(new_user) == User
        assert new_user.user_id == '00000000000000000000000000000000000' + str(len(repo.users))
        assert new_user.name == 'Vitor Soller'
        assert new_user.email == 'vitor@gmail.com'
        assert new_user.ra == None
        assert new_user.role == ROLE.EXTERNAL
        assert new_user.access_level == ACCESS_LEVEL.USER
        assert new_user.social_name == None
        assert new_user.accepted_terms == True
        assert new_user.accepted_notifications_sms == True
        assert new_user.accepted_notifications_email == True
        assert new_user.certificate_with_social_name == False
        assert new_user.phone == "+5511991758098"
        assert len(repo.users) == len_before + 1

    def test_create_user_usecase_wrong_access_level(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = User(user_id='000000000000000000000000000000000000', email='vitor@gmail.com', name='Vitor soller',
                    password="z12345",ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.ADMIN, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True, accepted_notifications_sms=True, certificate_with_social_name=False, phone="+5511991758098", accepted_notifications_email=True)

        with pytest.raises(EntityError):
            new_user = usecase(user)

    def test_create_user_usecase_duplicated_item(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = User(user_id='000000000000000000000000000000000000', email='zeeba@gmail.com', name='Vitor soller',
                    password="z12345", ra=None, role=ROLE.EXTERNAL, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True, accepted_notifications_sms=True,
                    certificate_with_social_name=False, phone="+5511991758098", accepted_notifications_email=True)

        with pytest.raises(DuplicatedItem):
            new_user = usecase(user)

    def test_create_user_usecase_terms_not_accepted(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = User(user_id='000000000000000000000000000000000000', email='zeeba@gmail.com', name='Vitor soller',
                    password="z12345", ra=None, role=ROLE.EXTERNAL, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=False, accepted_notifications_sms=True,
                    certificate_with_social_name=False, phone="+5511991758098", accepted_notifications_email=True)

        with pytest.raises(TermsNotAcceptedError):
            new_user = usecase(user)

    def test_create_user_strange_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):
            user = User(user_id='000000000000000000000000000000000000', email='zeeba@gmail.com', name='1=1vitor',
                        password="z12345", ra=None, role=ROLE.EXTERNAL, access_level=ACCESS_LEVEL.USER, created_at=None,
                        updated_at=None, social_name=None, accepted_terms=False, accepted_notifications_sms=True,
                        certificate_with_social_name=False, phone="+5511991758098", accepted_notifications_email=True)

    def test_create_user_strange_social_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):
            user = User(user_id='000000000000000000000000000000000000', email='zeeba@gmail.com', name='Vitor soller',
                        password="z12345", ra=None, role=ROLE.EXTERNAL, access_level=ACCESS_LEVEL.USER, created_at=None,
                        updated_at=None, social_name="1=1", accepted_terms=False, accepted_notifications_sms=True,
                        certificate_with_social_name=False, phone="+5511991758098", accepted_notifications_email=True)

    def test_create_user_usecase_social_name(self):

        user = User(user_id='000000000000000000000000000000000000', email='vitor@gmail.com', name='Vitor soller', password='z12345',
                    ra=None, role=ROLE.EXTERNAL, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True,
                    accepted_notifications_sms=True, certificate_with_social_name=True, phone="+5511991758098", accepted_notifications_email=True)
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):
            new_user = usecase(user)
