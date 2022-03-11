from datetime import datetime

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.entities.user import User
from src.infra.dtos.User.user_dto import CognitoUserDTO


class Test_CognitoUserDTO():

    def test_create_valid_user(self):
        user = User(name='Joao do Teste', cpfRne=12345678911, ra=19003315, role=ROLE.PROFESSOR,
                    accessLevel=ACCESS_LEVEL.ADMIN, createdAt=datetime(2022, 2, 15, 23, 15),
                    updatedAt=datetime(2022, 2, 15, 23, 15), email='bruno@bruno.com'
                    )

        userCognitoDto = CognitoUserDTO(user.dict())
        assert userCognitoDto.name == 'Joao Do Teste'
        assert userCognitoDto.cpfRne == 12345678911
        assert userCognitoDto.role == ROLE.PROFESSOR
        assert userCognitoDto.accessLevel == ACCESS_LEVEL.ADMIN
        assert userCognitoDto.ra == 19003315
        assert userCognitoDto.password is None
        assert userCognitoDto.email == 'bruno@bruno.com'
        userAttributes = userCognitoDto.userAttributes

        expectedAttributes = [
            {'Name': 'name', 'Value': 'Joao Do Teste'},
            {'Name': 'custom:cpfRne', 'Value': '12345678911'},
            {'Name': 'custom:ra', 'Value': '19003315'},
            {'Name': 'email', 'Value': 'bruno@bruno.com'},
            {'Name': 'custom:accessLevel', 'Value': ACCESS_LEVEL.ADMIN.value},
            {'Name': 'custom:role', 'Value': ROLE.PROFESSOR.value}
        ]
        for att in expectedAttributes:
            assert att in userAttributes

