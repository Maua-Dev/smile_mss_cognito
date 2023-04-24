from .refresh_token_controller import RefreshTokenController
from .refresh_token_usecase import RefreshTokenUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="refresh_token")

repo = Environments.get_user_repo()()
usecase = RefreshTokenUsecase(repo, observability=observability)
controller = RefreshTokenController(usecase, observability=observability)

@observability.presenter_decorators
def refresh_token_presenter(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = refresh_token_presenter(event, context)
    
    
    return response
