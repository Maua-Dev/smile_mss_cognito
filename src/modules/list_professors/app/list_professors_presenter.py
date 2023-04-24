from .list_professor_controller import ListProfessorsController
from .list_professors_usecase import ListProfessorsUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

observability = Environments.get_observability()(module_name="list_professors")

repo = Environments.get_user_repo()()
usecase = ListProfessorsUsecase(repo, observability=observability)
controller = ListProfessorsController(usecase, observability=observability)


@observability.presenter_decorators
def list_professors_presenter(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code, body=response.body, headers=response.headers)

    return httpResponse.toDict()

@observability.handler_decorators
def lambda_handler(event, context):
    
    response = list_professors_presenter(event, context)
    
    
    return response
