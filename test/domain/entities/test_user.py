from datetime import datetime

import pytest
from pydantic import ValidationError

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.entities.user import User
from src.domain.errors.errors import EntityError


class Test_User():

    def test_create_valid_user(self):
        user = User(name='Joao do Teste', cpfRne=75599469093, ra=19003315, role=ROLE.PROFESSOR,
                    accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                    updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                    socialName='Jonas', acceptedTerms=True, acceptedNotifications=True
                )

        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == ROLE.PROFESSOR
        assert user.accessLevel == ACCESS_LEVEL.ADMIN
        assert user.createdAt == datetime(2022, 2, 15, 23, 15)
        assert user.updatedAt == datetime(2022, 2, 15, 23, 15)
        assert user.ra == '19003315'
        assert user.password is None
        assert user.email == 'bruno@gmail.com'
        assert user.socialName == 'Jonas'
        assert user.acceptedTerms == True
        assert user.acceptedNotifications == True

    def test_create_valid_user2(self):
        user = User(name='Joao do Teste', cpfRne='01948697092', ra=19003315, role=ROLE.SPEAKER,
                    accessLevel=ACCESS_LEVEL.SPEAKER, createdAt=datetime(2022, 2, 15, 23, 15),
                    updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                    socialName='Jonas', acceptedTerms=True, acceptedNotifications=False
                )

        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == ROLE.SPEAKER
        assert user.accessLevel == ACCESS_LEVEL.SPEAKER
        assert user.createdAt == datetime(2022, 2, 15, 23, 15)
        assert user.updatedAt == datetime(2022, 2, 15, 23, 15)
        assert user.ra == '19003315'
        assert user.password is None
        assert user.socialName == 'Jonas'
        assert user.acceptedTerms == True
        assert user.acceptedNotifications == False

    def test_create_valid_user2(self):
        user = User(name='Joao do Teste', cpfRne='01948697092', ra=19003315, role=ROLE.SPEAKER,
                    accessLevel=ACCESS_LEVEL.SPEAKER, createdAt=datetime(2022, 2, 15, 23, 15),
                    updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                    acceptedTerms=True, acceptedNotifications=False
                )

        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == ROLE.SPEAKER
        assert user.accessLevel == ACCESS_LEVEL.SPEAKER
        assert user.createdAt == datetime(2022, 2, 15, 23, 15)
        assert user.updatedAt == datetime(2022, 2, 15, 23, 15)
        assert user.ra == '19003315'
        assert user.password is None
        assert user.acceptedTerms == True
        assert user.acceptedNotifications == False

    def test_create_valid_user3(self):
        user = User(name='Joao do Teste', cpfRne='01948697092', ra=19003315, role=ROLE.SPEAKER,
                    accessLevel=ACCESS_LEVEL.SPEAKER, createdAt=datetime(2022, 2, 15, 23, 15),
                    updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                    acceptedNotifications=False
                )

        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == ROLE.SPEAKER
        assert user.accessLevel == ACCESS_LEVEL.SPEAKER
        assert user.createdAt == datetime(2022, 2, 15, 23, 15)
        assert user.updatedAt == datetime(2022, 2, 15, 23, 15)
        assert user.ra == '19003315'
        assert user.password is None
        assert user.acceptedNotifications == False

    def test_create_valid_user4(self):
        user = User(name='Joao do Teste', cpfRne='01948697092', ra=19003315, role=ROLE.SPEAKER,
                    accessLevel=ACCESS_LEVEL.SPEAKER, createdAt=datetime(2022, 2, 15, 23, 15),
                    updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                    acceptedTerms=True
                )

        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == ROLE.SPEAKER
        assert user.accessLevel == ACCESS_LEVEL.SPEAKER
        assert user.createdAt == datetime(2022, 2, 15, 23, 15)
        assert user.updatedAt == datetime(2022, 2, 15, 23, 15)
        assert user.ra == '19003315'
        assert user.password is None
        assert user.acceptedTerms == True

    def test_create_valid_user5(self):
        user = User(name='Joao do Teste', cpfRne='01948697092', ra=19003315, role=ROLE.SPEAKER,
                    accessLevel=ACCESS_LEVEL.SPEAKER, createdAt=datetime(2022, 2, 15, 23, 15),
                    updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                    acceptedTerms=None)

        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == ROLE.SPEAKER
        assert user.accessLevel == ACCESS_LEVEL.SPEAKER
        assert user.createdAt == datetime(2022, 2, 15, 23, 15)
        assert user.updatedAt == datetime(2022, 2, 15, 23, 15)
        assert user.ra == '19003315'
        assert user.password is None

    def test_create_invalid_user1(self):
        with pytest.raises(EntityError):
            User(name='', cpfRne=75599469093, ra=19003315, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), socialName=None,
                 )

    def test_create_invalid_user2(self):
        with pytest.raises(EntityError):
            User(name='Joao do teste', cpfRne=7559946909, ra=19003315, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15)
                 )

    def test_create_invalid_user3(self):
        with pytest.raises(EntityError):
            User(name='Joao do teste', cpfRne=1234567891, ra=19003315, role="PROFESSOR",
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15)
                 )

    def test_create_invalid_user4(self):
        with pytest.raises(EntityError):
            User(name='Joao do Teste', cpfRne=75599469093, ra=19003315, role=ROLE.PROFESSOR,
                 accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), email="bruno@"
                 )

    def test_create_invalid_user5(self):
        with pytest.raises((EntityError, ValidationError)):
            User(name='Joao do Teste', cpfRne='01948697092', ra=19003315, role=ROLE.SPEAKER,
                 accessLevel=ACCESS_LEVEL.SPEAKER, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                 socialName='Jonas', acceptedTerms="teste", acceptedNotifications=False
                 )

    def test_create_invalid_user6(self):
        with pytest.raises((EntityError, ValidationError)):
            User(name='Joao do Teste', cpfRne='01948697092', ra=19003315, role=ROLE.SPEAKER,
                 accessLevel=ACCESS_LEVEL.SPEAKER, createdAt=datetime(2022, 2, 15, 23, 15),
                 updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                 socialName='Jonas', acceptedTerms=True, acceptedNotifications="teste"
                 )

    def test_create_invalid_user7(self):
        with pytest.raises((EntityError, ValidationError)):
            User(name='Joao do Teste', cpfRne=75599469093, ra=19003315, role=ROLE.PROFESSOR,
                        accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                        updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@gmail.com',
                        socialName='Jonas', acceptedTerms=False, acceptedNotifications=True
                    )