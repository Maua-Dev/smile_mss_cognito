from src.modules.check_token.app.check_token_viewmodel import CheckTokenViewmodel
from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User


class Test_CheckTokenViewmodel:

    def test_check_token_viewmodel(self):
        viewmodel = CheckTokenViewmodel(
            role=ROLE.STUDENT,
            access_level=ACCESS_LEVEL.USER,
            email='zeeba@gmail.com',
            valid_token=True,
            user_id='0001'
        )

        expected = {
            'role': ROLE.STUDENT,
            'access_level': ACCESS_LEVEL.USER,
            'email': 'zeeba@gmail.com',
            'valid_token': True,
            'user_id': '0001'
        }

        assert viewmodel.to_dict() == expected
