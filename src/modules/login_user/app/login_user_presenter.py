from .login_user_controller import LoginUserController
from .login_user_usecase import LoginUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="login_user")

repo = Environments.get_user_repo()()
usecase = LoginUserUsecase(repo, observability=observability)
controller = LoginUserController(usecase, observability=observability)

@observability.presenter_decorators
def login_user_presenter(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = login_user_presenter(event, context)
    
    
    return response
