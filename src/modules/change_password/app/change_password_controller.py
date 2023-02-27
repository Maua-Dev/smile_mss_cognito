from .change_password_usecase import ChangePasswordUsecase
from .change_password_viewmodel import ChangePasswordViewmodel

from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction, UserNotConfirmed, InvalidCredentials
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden, \
    Unauthorized


class ChangePasswordController:
    def __init__(self, usecase: ChangePasswordUsecase):
        self.ChangePasswordUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        if not request.data:
            return BadRequest("Não existe corpo da requisição.")
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')

            resp = self.ChangePasswordUsecase(
                email=request.data.get('email')
            )

            viewmodel = ChangePasswordViewmodel(resp)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:

            return Forbidden(body=f"Ação não permitida: {err.message}")

        except UserNotConfirmed as err:

            return Unauthorized(body="Usuário não confirmado")

        except InvalidCredentials as err:

            return Forbidden(body="Usuário ou senha inválidos")

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:

            return InternalServerError(body=err.args[0])
