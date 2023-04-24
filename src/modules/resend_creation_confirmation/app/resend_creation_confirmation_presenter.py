from .resend_creation_confirmation_controller import ResendCreationConfirmationController
from .resend_creation_confirmation_usecase import ResendCreationConfirmationUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="resend_creation_confirmation")

repo = Environments.get_user_repo()()
usecase = ResendCreationConfirmationUsecase(repo, observability=observability)
controller = ResendCreationConfirmationController(usecase, observability=observability)

@observability.presenter_decorators
def resend_creation_confirmation_presenter(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = resend_creation_confirmation_presenter(event, context)
    
    
    return response
