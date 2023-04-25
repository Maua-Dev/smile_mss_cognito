import json
from src.shared.domain.observability.observability_interface import IObservability
from .delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, UserNotConfirmed
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError, NotFound, \
    Unauthorized


class DeleteUserController:
    def __init__(self, usecase: DeleteUserUsecase, observability: IObservability) -> None:
        self.usecase = usecase
        self.observability = observability

    def __call__(self, req: IRequest) -> IResponse:
        self.observability.log_controller_in()

        if req.data is None:
            raise MissingParameters('Missing body.')

        if 'email' not in req.data:
            raise MissingParameters('Missing email.')
        try:
            self.usecase(req.data.get('email'))
            response = OK('User deleted.')

            self.observability.log_controller_out(input=json.dumps(response.body), status_code=response.status_code)
            return response

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)
            return Forbidden(body=err.message)

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=err.message)

        except NoItemsFound as err:
            self.observability.log_exception(status_code=404, exception_name="NoItemsFound", message=err.message)

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except UserNotConfirmed as err:
            self.observability.log_exception(status_code=401, exception_name="UserNotConfirmed", message=err.message)
            return Unauthorized(body="Usuário não confirmado")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])
