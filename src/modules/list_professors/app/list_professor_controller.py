import json
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from .list_professor_viewmodel import ListProfessorsViewmodel
from .list_professors_usecase import ListProfessorsUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, Forbidden, NotFound


class ListProfessorsController:
    def __init__(self, usecase: ListProfessorsUsecase, observability: IObservability) -> None:
        self.usecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()

            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('access_token')
            access_token = token[1]

            list_professor = self.usecase(access_token=access_token)

            viewmodel = ListProfessorsViewmodel(list_professor)
            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=json.dumps(response.body), status_code=response.status_code)
            
            return response

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetros ausentes: {err.message}")

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)

            return Forbidden(body="Apenas administradores podem acessar essa funcionalidade")

        except NoItemsFound as err:
            self.observability.log_exception(status_code=404, exception_name="NoItemsFound", message=err.message)

            return NotFound(body="Usuário não encontrado")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=f"Erro inesperado: {err.args[0]}")
