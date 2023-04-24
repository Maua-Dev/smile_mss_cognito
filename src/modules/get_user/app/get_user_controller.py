import json
from src.shared.domain.observability.observability_interface import IObservability
from .get_user_usecase import GetUserUsecase
from .get_user_viewmodel import GetUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetUserController:

    def __init__(self, usecase: GetUserUsecase, observability: IObservability):
        self.GetUserUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            
            if request.data.get('email') is None:
                raise MissingParameters('email')

            user = self.GetUserUsecase(
                email=request.data.get('email')
            )

            viewmodel = GetUserViewmodel(user)

            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=json.dumps(response.body))
            
            return response

        except NoItemsFound as err:
            self.observability.log_exception(status_code=404, exception_name="NoItemsFound", message=err.message)

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:

            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])
            return InternalServerError(body=err.args[0])

