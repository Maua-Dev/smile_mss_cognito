from .refresh_token_usecase import RefreshTokenUsecase
from .refresh_token_viewmodel import RefreshTokenViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError


class RefreshTokenController:

    def __init__(self, usecase: RefreshTokenUsecase):
        self.refreshTokenUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
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
            return OK(refresh_token_viewmodel.to_dict())

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:

            return Forbidden(body=f"Sem autorização para: {err.message}")

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:

            return InternalServerError(body=err.args[0])

