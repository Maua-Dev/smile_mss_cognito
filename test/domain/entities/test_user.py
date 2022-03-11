from datetime import datetime

import pytest

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.entities.user import User
from src.domain.errors.errors import EntityError

class Test_User():

    def test_create_valid_user(self):
        user =  User(name='Joao do Teste', cpfRne=12345678911, ra=19003315, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com'
                )
        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == ROLE.PROFESSOR
        assert user.accessLevel == ACCESS_LEVEL.ADMIN
        assert user.createdAt == datetime(2022, 2, 15, 23, 15)
        assert user.updatedAt == datetime(2022, 2, 15, 23, 15)
        assert user.ra == 19003315
        assert user.password is None




    def test_create_invalid_student1(self):
        with pytest.raises(EntityError):
            User(name='', cpfRne=12345678911, ra=19003315, role=ROLE.PROFESSOR,
                accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                updatedAt=datetime(2022, 2, 15, 23, 15)
            )

    def test_create_invalid_student2(self):
        with pytest.raises(EntityError):
            User(name='Joao do teste', cpfRne=1234567891, ra=19003315, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15)
             )

    def test_create_invalid_student3(self):
        with pytest.raises(EntityError):
            User(name='Joao do teste', cpfRne=1234567891, ra=19003315, role="PROFESSOR",
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15)
            )

    def test_create_invalid_student4(self):
        with pytest.raises(EntityError):
            User(name='Joao do Teste', cpfRne=12345678911, ra=19003315, role=ROLE.PROFESSOR,
                        accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                        updatedAt=datetime(2022, 2, 15, 23, 15), email="bruno@"
                        )

