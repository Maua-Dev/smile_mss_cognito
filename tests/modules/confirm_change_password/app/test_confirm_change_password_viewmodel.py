from src.modules.confirm_change_password.app.confirm_change_password_viewmodel import ConfirmChangePasswordViewmodel


class Test_ConfirmChangePasswordViewmodel:

    def test_confirm_change_password_viewmodel(self):
        viewmodel = ConfirmChangePasswordViewmodel(
            result=True, message=''
        )

        expected = {
            'result': True,
            'message': ''
        }

        assert viewmodel.to_dict() == expected
