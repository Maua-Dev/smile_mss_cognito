
from .confirm_user_creation_controller import ConfirmUserCreationController
from .confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


repo = Environments.get_user_repo()()
usecase = ConfirmUserCreationUsecase(repo)
controller = ConfirmUserCreationController(usecase)


def lambda_handler(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()
