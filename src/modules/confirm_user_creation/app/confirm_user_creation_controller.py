import json
import os
from src.shared.domain.observability.observability_interface import IObservability

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from .confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, UserAlreadyConfirmed, ForbiddenAction, \
    InvalidCredentials, UserNotConfirmed
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound, \
    RedirectResponse, Forbidden, Unauthorized


class ConfirmUserCreationController:
    def __init__(self, usecase: ConfirmUserCreationUsecase, observability: IObservability) -> None:
        self.usecase = usecase
        self.observability = observability

    def __call__(self, req: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            
            result = self.usecase(
                email=req.data.get('email'),
                confirmation_code=req.data.get('confirmation_code')
            )

            front_endpoint = os.environ.get('FRONT_ENDPOINT')

            if not result:
                self.observability.log_exception(status_code=400, exception_name="EntityError", message="User not found or invalid code.")
                
                message = "User not found or invalid code."
                return BadRequest(message)
            
            response = RedirectResponse(
                body={
                    "location": f"{front_endpoint}/#/login/cadastro/sucesso"
                }
            )

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

        except UserAlreadyConfirmed as err:
            self.observability.log_exception(status_code=403, exception_name="UserAlreadyConfirmed", message=err.message)
            return Forbidden(body="Usuário já confirmado")

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)
            return Forbidden(body=f"Ação não permitida: {err.message}")

        except InvalidCredentials as err:
            self.observability.log_exception(status_code=403, exception_name="InvalidCredentials", message=err.message)
            return Forbidden(body=f"Usuário ou senha inválidos" if err.message != "confirmation_code" else f"Código de confirmção inválido")

        except UserNotConfirmed as err:
            self.observability.log_exception(status_code=401, exception_name="UserNotConfirmed", message=err.message)
            return Unauthorized(body="Usuário não confirmado")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])

