import json
from src.shared.domain.observability.observability_interface import IObservability
from .confirm_change_password_usecase import ConfirmChangePasswordUsecase
from .confirm_change_password_viewmodel import ConfirmChangePasswordViewmodel

from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, UserNotConfirmed, InvalidCredentials
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, \
    Unauthorized, Forbidden


class ConfirmChangePasswordController:
    def __init__(self, usecase: ConfirmChangePasswordUsecase, observability: IObservability):
        self.usecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:

        try:
            self.observability.log_controller_in()
            
            if request.data.get('email') is None:
                raise MissingParameters('email')
            if request.data.get('new_password') is None:
                raise MissingParameters('new_password')
            if request.data.get('confirmation_code') is None:
                raise MissingParameters('confirmation_code')

            resp = self.usecase(
                email=request.data.get('email'),
                confirmation_code=request.data.get('confirmation_code'),
                new_password=request.data.get('new_password')
            )

            viewmodel = ConfirmChangePasswordViewmodel(resp)

            if not resp:
                viewmodel.message = "User not found, invalid confirmation code or weak new password."
                self.observability.log_exception(status_code=400, exception_name="EntityError", message=viewmodel.message)
                
                return BadRequest(viewmodel.to_dict())
            response = OK(viewmodel.to_dict())

            self.observability.log_controller_out(input=json.dumps(response.body))
            return response

        except NoItemsFound as err:
            self.observability.log_exception(status_code=404, exception_name="NoItemsFound", message=err.message)

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except UserNotConfirmed as err:
            self.observability.log_exception(status_code=401, exception_name="UserNotConfirmed", message=err.message)
            return Unauthorized(body="Usuário não confirmado")

        except InvalidCredentials as err:
            self.observability.log_exception(status_code=403, exception_name="InvalidCredentials", message=err.message)
            return Forbidden(body="Código de confirmação inválido" if err.message == "confirmation_code" else "Usuário ou senha inválidos")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name="InternalServerError", message=err.args[0])
            return InternalServerError(body=err.args[0])
