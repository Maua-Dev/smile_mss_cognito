import json
from src.shared.domain.observability.observability_interface import IObservability
from .refresh_token_usecase import RefreshTokenUsecase
from .refresh_token_viewmodel import RefreshTokenViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidTokenError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError


class RefreshTokenController:

    def __init__(self, usecase: RefreshTokenUsecase, observability: IObservability):
        self.refreshTokenUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('access_token')
            refresh_token = token[1]

            tokens = self.refreshTokenUsecase(refresh_token)
            access_token, refresh_token, id_token = tokens
            refresh_token_viewmodel = RefreshTokenViewmodel(
                access_token=access_token, refresh_token=refresh_token, id_token=id_token)
            
            
            response = OK(refresh_token_viewmodel.to_dict())

            self.observability.log_controller_out(input=json.dumps(response.body))
            
            return response

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)
            return Forbidden(body=f"Sem autorização para: {err.message}")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except InvalidTokenError as err:
            self.observability.log_exception(status_code=400, exception_name="InvalidTokenError", message=err.message)
            return BadRequest(body=f"Token inválido, favor fazer login novamente")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])

