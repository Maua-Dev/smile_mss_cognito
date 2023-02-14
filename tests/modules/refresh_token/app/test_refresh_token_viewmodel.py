from src.modules.refresh_token.app.refresh_token_viewmodel import RefreshTokenViewmodel


class Test_RefreshTokenViewmodel:

    def test_refresh_token_viewmodel(self):
        access_token = 'valid_access_token-vitor@maua.br'
        refresh_token = "valid_refresh_token-vitor@maua.br"

        tokens = RefreshTokenViewmodel(access_token, refresh_token)

        expected = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': "Token refreshed successfully"
        }

        assert tokens.to_dict() == expected
