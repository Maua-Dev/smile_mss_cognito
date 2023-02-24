from .delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError


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

        except Exception as err:

            return InternalServerError(body=err.args[0])
