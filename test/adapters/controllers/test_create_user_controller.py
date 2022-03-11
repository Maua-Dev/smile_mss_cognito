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
            "cpfRne": 12345678913,
            "ra": 20001236,
            "role": ROLE.PROFESSOR,
            "email": "user@teste.com",
            "accessLevel": ACCESS_LEVEL.ADMIN,
            "createdAt": datetime(2022, 2, 15, 23, 15),
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "password": '123456'
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_invalid_cpfRne_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpfRne": 12345678,
            "ra": 20001236,
            "role": '',
            "accessLevel": '',
            "createdAt": datetime(2022, 2, 15, 23, 15),
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "password": '123456'
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_ra_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpfRne": 12345678913,
            "ra": 205001236,
            "role": '',
            "accessLevel": '',
            "createdAt": datetime(2022, 2, 15, 23, 15),
            "updatedAt": datetime(2022, 2, 15, 23, 15)
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_ra2_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpfRne": 12345678913,
            "ra": 19.00331-5,
            "role": '',
            "accessLevel": '',
            "createdAt": datetime(2022, 2, 15, 23, 15),
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "password": '123456'
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_role_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpfRne": 12345678913,
            "ra": 19003315,
            "role": 'qualquerCoisa',
            "accessLevel": '',
            "createdAt": datetime(2022, 2, 15, 23, 15),
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "password": '123456'
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_create_invalid_date_user_controller(self):
        request = HttpRequest(body={
            "name": 'user3',
            "cpfRne": 12345678913,
            "ra": 19003315,
            "role": 'qualquerCoisa',
            "accessLevel": '',
            "createdAt": "2022-02-15T23:15",
            "updatedAt": datetime(2022, 2, 15, 23, 15),
            "password": '123456'
        })

        createUserController = CreateUserController(UserRepositoryMock())
        response = await createUserController(request)
        assert response.status_code == 400