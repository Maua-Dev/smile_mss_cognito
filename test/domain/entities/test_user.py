import pytest
from src.domain.entities.user import User
from src.domain.errors.errors import EntityError

class Test_Student():

    def test_create_valid_user(self):
        user = User(name='Joao do teste', cpfRne=12345678910, role="Student")
        assert len(user.name) > 0
        assert user.name == 'Joao Do Teste'
        assert len(str(user.cpfRne)) == 11
        assert user.role == "Student"

    def test_create_invalid_student1(self):
        with pytest.raises(EntityError):
            User(name='', cpfRne=12345678910, role="Student")

    def test_create_invalid_student2(self):
        with pytest.raises(EntityError):
            User(name='Joao do teste', cpfRne=1234567891, role="Student")

    def test_create_invalid_student3(self):
        with pytest.raises(EntityError):
            User(name='Joao do teste', cpfRne=12345678910, role="")

