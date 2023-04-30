from .confirm_change_password_controller import ConfirmChangePasswordController
from .confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="confirm_change_password")

repo = Environments.get_user_repo()()
usecase = ConfirmChangePasswordUsecase(repo, observability=observability)
controller = ConfirmChangePasswordController(usecase, observability=observability)


@observability.presenter_decorators
def confirm_change_password_presenter(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = confirm_change_password_presenter(event, context)
    observability.add_error_count_metric(statusCode=response.get('statusCode', 500))
    
    return response