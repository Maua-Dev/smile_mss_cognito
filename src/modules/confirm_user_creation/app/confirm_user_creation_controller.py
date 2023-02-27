import os

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
    def __init__(self, usecase: ConfirmUserCreationUsecase) -> None:
        self.usecase = usecase

    def __call__(self, req: IRequest) -> IResponse:
        try:
            result = self.usecase(
                email=req.data.get('email'),
                confirmation_code=req.data.get('confirmation_code')
            )

            front_endpoint = os.environ.get('FRONT_ENDPOINT')

            if not result:
                message = "User not found or invalid code."
                return BadRequest(message)

            return RedirectResponse(
                body={
                    "location": f"{front_endpoint}/#/login/cadastro/sucesso"
                }
            )

        except NoItemsFound as err:

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except UserAlreadyConfirmed as err:

            return Forbidden(body="Usuário já confirmado")

        except ForbiddenAction as err:

            return Forbidden(body=f"Ação não permitida: {err.message}")

        except InvalidCredentials as err:

            return Forbidden(body=f"Usuário ou senha inválidos" if err.message != "confirmation_code" else f"Código de confirmção inválido")

        except UserNotConfirmed as err:

            return Unauthorized(body="Usuário não confirmado")

        except Exception as err:

            return InternalServerError(body=err.args[0])

