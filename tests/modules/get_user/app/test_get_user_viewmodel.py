from src.modules.get_user.app.get_user_viewmodel import GetUserViewmodel
from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User


class Test_GetUserViewmodel:

    def test_get_user_viewmodel(self):
        user = User(user_id='000000000000000000000000000000000001', email='zeeba@gmail.com', name='Caio soller', password='z12345',
                    ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=16449777000,
                    updated_at=16449777000, social_name='zeeba toledo', accepted_terms=True,
                    accepted_notifications=True, certificate_with_social_name=True, phone="5511991758098")

        expected = {
            'user': {
                'user_id': '000000000000000000000000000000000001',
                'name': 'Caio Soller',
                'email': 'zeeba@gmail.com',
                'ra': '20014309',
                'role': 'STUDENT',
                'access_level': 'USER',
                'social_name': 'Zeeba Toledo',
                "phone": "5511991758098",
            },
            'message': 'the user was retrieved'
        }

        viewmodel = GetUserViewmodel(user)

        assert viewmodel.to_dict() == expected
