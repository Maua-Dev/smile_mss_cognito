import json
from src.shared.domain.observability.observability_interface import IObservability
from .resend_creation_confirmation_usecase import ResendCreationConfirmationUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, UserNotConfirmed, UserAlreadyConfirmed, \
    ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, \
    Unauthorized, Forbidden
from .resend_creation_confirmation_viewmodel import ResendCreationConfirmationViewmodel


class ResendCreationConfirmationController:

    def __init__(self, usecase: ResendCreationConfirmationUsecase, observability: IObservability):
        self.ResendConfirmationUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            
            if request.data.get('email') is None:
                raise MissingParameters('email')

            result = self.ResendConfirmationUsecase(
                email=request.data.get('email')
            )

            viewmodel = ResendCreationConfirmationViewmodel()
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

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)
            return Forbidden(body=f"Ação não permitida: {err.message}")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except UserAlreadyConfirmed as err:
            self.observability.log_exception(status_code=403, exception_name="UserAlreadyConfirmed", message=err.message)
            return Forbidden(body="Usuário já confirmado")


        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])


