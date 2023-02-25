from .delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound, UserNotConfirmed
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError, NotFound, \
    Unauthorized


class DeleteUserController:
    def __init__(self, usecase: DeleteUserUsecase) -> None:
        self.usecase = usecase

    def __call__(self, req: IRequest) -> IResponse:

        if req.data is None:
            raise MissingParameters('Missing body.')

        if 'email' not in req.data:
            raise MissingParameters('Missing email.')
        try:
            self.usecase(req.data.get('email'))
            return OK('User deleted.')

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:

            return Forbidden(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except NoItemsFound as err:

            return NotFound(body='Nenhum usuário econtrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except UserNotConfirmed as err:

            return Unauthorized(body="Usuário não confirmado")

        except Exception as err:

            return InternalServerError(body=err.args[0])
