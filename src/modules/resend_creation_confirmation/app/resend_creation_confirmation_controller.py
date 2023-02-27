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

    def __init__(self, usecase: ResendCreationConfirmationUsecase):
        self.ResendConfirmationUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')

            result = self.ResendConfirmationUsecase(
                email=request.data.get('email')
            )

            viewmodel = ResendCreationConfirmationViewmodel()

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except UserNotConfirmed as err:

            return Unauthorized(body="Usuário não confirmado")

        except ForbiddenAction as err:

            return Forbidden(body=f"Ação não permitida: {err.message}")

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except UserAlreadyConfirmed as err:
            return Forbidden(body="Usuário já confirmado")


        except Exception as err:

            return InternalServerError(body=err.args[0])


