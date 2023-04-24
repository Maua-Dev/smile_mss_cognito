import json
import urllib.parse

from src.shared.domain.observability.observability_interface import IObservability
from .change_password_usecase import ChangePasswordUsecase
from .change_password_viewmodel import ChangePasswordViewmodel

from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction, UserNotConfirmed, InvalidCredentials
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden, \
    Unauthorized


class ChangePasswordController:
    def __init__(self, usecase: ChangePasswordUsecase, observability: IObservability):
        self.ChangePasswordUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        self.observability.log_controller_in()

        if not request.data:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message="Não existe corpo da requisição.")
            
            return BadRequest("Não existe corpo da requisição.")
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')

            email = urllib.parse.unquote(request.data.get('email'))

            resp = self.ChangePasswordUsecase(
                email=email
            )

            viewmodel = ChangePasswordViewmodel(resp)
            response = OK(viewmodel.to_dict())

            self.observability.log_controller_out(input=json.dumps(response.body))
            return response

        except NoItemsFound as err:
            self.observability.log_exception(status_code=404, exception_name="NoItemsFound", message=err.message)

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)
            return Forbidden(body=f"Ação não permitida: {err.message}")

        except UserNotConfirmed as err:
            self.observability.log_exception(status_code=401, exception_name="UserNotConfirmed", message=err.message)
            return Unauthorized(body="Usuário não confirmado")

        except InvalidCredentials as err:
            self.observability.log_exception(status_code=403, exception_name="InvalidCredentials", message=err.message)
            return Forbidden(body="Usuário ou senha inválidos")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])
