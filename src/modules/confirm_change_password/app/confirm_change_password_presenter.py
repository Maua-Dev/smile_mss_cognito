from .confirm_change_password_controller import ConfirmChangePasswordController
from .confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_activity_repo()()
usecase = ConfirmChangePasswordUsecase(repo)
controller = ConfirmChangePasswordController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
