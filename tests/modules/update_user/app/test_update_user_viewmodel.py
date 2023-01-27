from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User


class Test_UpdateUserViewModel:

    def test_update_user_viewmodel(self):
        user = User(user_id='0001', email='zeeba@gmail.com', name='Caio soller', password='z12345',
                    ra='20014309', role=ROLE.STUDENT, access_level=ACCESS_LEVEL.USER, created_at=1644977700000,
                    updated_at=1644977700000, social_name='zeeba toledo', accepted_terms=True,
                    accepted_notifications=True, certificate_with_social_name=True
                    )

        update_user_viewmodel = UpdateUserViewmodel(user)

        expected = {
            'user': {
                'user_id': '0001',
                'name': 'Caio Soller',
                'email': 'zeeba@gmail.com',
                'ra': '20014309',
                'role': 'STUDENT',
                'access_level': 'USER',
                'social_name': 'Zeeba Toledo',
                'certificate_with_social_name': True,
                'accepted_notifications': True
            },
            'message': 'the user was updated'
        }

        assert update_user_viewmodel.to_dict() == expected
