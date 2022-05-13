from datetime import datetime

import pytest

from src.adapters.controllers.create_user_controller import CreateUserController
from src.adapters.helpers.http_models import HttpRequest
from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.infra.repositories.user_repository_mock import UserRepositoryMock


class TestCreateUserController:

    @pytest.mark.asyncio
    async def test_create_valid_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpf_rne": '46864806049',
            "ra": '20001236',
            "role": ROLE.PROFESSOR.value,
            "email": "user@teste.com",
            "access_level": ACCESS_LEVEL.USER.value,
            "password": '123456',
            "accepted_terms": True,
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_invalid_cpfRne_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpf_rne": '46864806149',
            "ra": '20001236',
            "role": '',
            "access_level": '',
            "password": '123456',
            "accepted_terms": True,
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_ra_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpf_rne": '49975288030',
            "ra": '205001236',
            "role": '',
            "access_level": '',
            "createdAt": datetime(2022, 2, 15, 23, 15),
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "accepted_terms": True,
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_ra2_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpf_rne": '49975288030',
            "ra": 19.00331-5,
            "role": '',
            "access_level": '',
            "password": '123456',
            "accepted_terms": True,
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_role_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpf_rne": '11315156091',
            "ra": '19003315',
            "role": 'qualquerCoisa',
            "access_level": '',
            "createdAt": datetime(2022, 2, 15, 23, 15),
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "password": '123456',
            "accepted_terms": True,
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_date_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpf_rne": '11315156091',
            "ra": '19003315',
            "role": 'qualquerCoisa',
            "access_level": '',
            "createdAt": "2022-02-15T23:15",
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "password": '123456',
            "accepted_terms": True,
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_missing_terms_user_controller(self):
        request = HttpRequest(body={
            "name": 'user4',
            "cpf_rne": '61046498070',
            "ra": '20001236',
            "role": ROLE.PROFESSOR.value,
            "email": "user@teste.com",
            "access_level": ACCESS_LEVEL.ADMIN.value,
            "password": '123456',
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_with_admin_level_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpf_rne": '46864806049',
            "ra": '20001236',
            "role": ROLE.PROFESSOR.value,
            "email": "user@teste.com",
            "access_level": ACCESS_LEVEL.ADMIN.value,
            "password": '123456',
            "accepted_terms": True,
            "accepted_notifications": True
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400