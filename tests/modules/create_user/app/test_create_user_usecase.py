import pytest

from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.shared.domain.entities.user import User
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserUsecase:
    def test_create_user_usecase(self):

        user = User(user_id='000000000000000000000000000000000000', email='vitor@gmail.com', name='Vitor soller', password='z12345',
                    ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True,
                    accepted_notifications=True, certificate_with_social_name=False, phone="5511991758098")
        repo = UserRepositoryMock()
        len_before = len(repo.users)
        usecase = CreateUserUsecase(repo)

        new_user = usecase(user)

        assert type(new_user) == User
        assert new_user.user_id == '00000000000000000000000000000000000' + str(len(repo.users))
        assert new_user.name == 'Vitor Soller'
        assert new_user.email == 'vitor@gmail.com'
        assert new_user.ra == None
        assert new_user.role == ROLE.STUDENT
        assert new_user.access_level == ACCESS_LEVEL.USER
        assert new_user.social_name == None
        assert new_user.accepted_terms == True
        assert new_user.accepted_notifications == True
        assert new_user.certificate_with_social_name == False
        assert new_user.phone == "5511991758098"
        assert len(repo.users) == len_before + 1

    def test_create_user_usecase_missing_required_field(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = User(user_id='000000000000000000000000000000000000', email='vitor@gmail.com', name='Vitor soller',
                    password='z12345',
                    ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True,
                    accepted_notifications=None, certificate_with_social_name=False, phone="5511991758098")

        with pytest.raises(ForbiddenAction):
            new_user = usecase(user)

    def test_create_user_usecase_wrong_access_level(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = User(user_id='000000000000000000000000000000000000', email='vitor@gmail.com', name='Vitor soller',
                    password="z12345",ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.ADMIN, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True, accepted_notifications=True, certificate_with_social_name=False, phone="5511991758098")

        with pytest.raises(EntityError):
            new_user = usecase(user)

    def test_create_user_usecase_duplicated_item(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        user = User(user_id='000000000000000000000000000000000000', email='zeeba@gmail.com', name='Vitor soller',
                    password="z12345", ra=None, role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=None,
                    updated_at=None, social_name=None, accepted_terms=True, accepted_notifications=True,
                    certificate_with_social_name=False, phone="5511991758098")

        with pytest.raises(DuplicatedItem):
            new_user = usecase(user)
