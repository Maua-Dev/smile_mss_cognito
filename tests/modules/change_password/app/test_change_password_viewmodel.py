from src.modules.change_password.app.change_password_viewmodel import ChangePasswordViewmodel


class Test_ChangePasswordViewmodel:

    def test_change_password_viewmodel(self):
        viewmodel = ChangePasswordViewmodel(
            result=True, message=''
        )

        expected = {
            'result': True,
            'message': ''
        }

        assert viewmodel.to_dict() == expected
