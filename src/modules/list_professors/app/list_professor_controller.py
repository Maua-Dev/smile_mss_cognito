import json
from src.shared.domain.observability.observability_interface import IObservability
from .list_professor_viewmodel import ListProfessorsViewmodel
from .list_professors_usecase import ListProfessorsUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class ListProfessorsController:
    def __init__(self, usecase: ListProfessorsUsecase, observability: IObservability) -> None:
        self.usecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()

            list_professor = self.usecase()

            viewmodel = ListProfessorsViewmodel(list_professor)
            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=json.dumps(response.body))
            
            return response

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])
