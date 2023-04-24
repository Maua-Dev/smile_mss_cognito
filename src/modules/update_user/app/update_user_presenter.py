from .update_user_controller import UpdateUserController
from .update_user_usecase import UpdateUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="update_user")

repo = Environments.get_user_repo()()
usecase = UpdateUserUsecase(repo, observability=observability)
controller = UpdateUserController(usecase, observability=observability)

@observability.presenter_decorators
def update_user_presenter(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = update_user_presenter(event, context)
    
    
    return response

