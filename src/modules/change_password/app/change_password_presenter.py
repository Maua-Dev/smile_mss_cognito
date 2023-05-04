from src.shared.environments import Environments
from .change_password_controller import ChangePasswordController
from .change_password_usecase import ChangePasswordUsecase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="change_password")

repo = Environments.get_user_repo()()
usecase = ChangePasswordUsecase(repo, observability=observability)
controller = ChangePasswordController(usecase, observability=observability)


@observability.presenter_decorators
def change_password_presenter(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    response = change_password_presenter(event, context)
    observability.add_error_count_metric(statusCode=response.get('statusCode', 500))
    
    
    return response
