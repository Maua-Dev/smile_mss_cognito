
from .confirm_user_creation_controller import ConfirmUserCreationController
from .confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="confirm_user_creation")

repo = Environments.get_user_repo()()
usecase = ConfirmUserCreationUsecase(repo, observability=observability)
controller = ConfirmUserCreationController(usecase, observability=observability)


@observability.presenter_decorators
def confirm_user_creation_presenter(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = confirm_user_creation_presenter(event, context)
    
    
    return response
