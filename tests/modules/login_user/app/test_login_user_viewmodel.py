from src.modules.login_user.app.login_user_viewmodel import LoginUserViewmodel


class Test_LoginUserViewmodel:
    def test_login_user_viewmodel(self):
        data = {
            'user_id': '000000000000000000000000000000000002',
            'email': 'vitor@maua.br',
            'name': 'Vitor Branco',
            'ra': '20014309',
            'role': 'STUDENT',
            'access_level': 'ADMIN',
            'created_at': 16449777000,
            'updated_at': 16449777000,
            'social_name': 'Zeeba Toledo',
            'accepted_terms': True,
            'accepted_notifications': True,
            'certificate_with_social_name': False,
            'phone': '5511991758098',
            'access_token': 'valid_access_token-vitor@maua.br',
            'refresh_token': 'valid_refresh_token-vitor@maua.br'
        }

        login_user_viewmodel = LoginUserViewmodel(data)

        expected = {
            'user': {
                'access_token': 'valid_access_token-vitor@maua.br',
                'refresh_token': 'valid_refresh_token-vitor@maua.br',
                'ra': '20014309',
                'role': 'STUDENT',
                'access_level': 'ADMIN',
                'email': 'vitor@maua.br',
                'phone': '5511991758098',
                'social_name': 'Zeeba Toledo',
                'name': 'Vitor Branco',
                'certificate_with_social_name': False,
                'user_id': '000000000000000000000000000000000002',
            },
            'message': 'Login successful'
        }

        assert login_user_viewmodel.to_dict() == expected