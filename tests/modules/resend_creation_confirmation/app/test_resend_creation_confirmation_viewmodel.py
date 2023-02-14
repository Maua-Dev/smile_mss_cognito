from src.modules.resend_creation_confirmation.app.resend_creation_confirmation_viewmodel import \
    ResendCreationConfirmationViewmodel


class Test_ResendConfirmationViewmodel:
    def test_resend_confirmation_viewmodel(self):
        viewmodel = ResendCreationConfirmationViewmodel()

        expected = {'message': 'the email was sent'}


        assert viewmodel.to_dict() == expected

