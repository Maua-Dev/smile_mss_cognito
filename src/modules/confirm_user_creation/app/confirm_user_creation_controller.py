from src.shared.domain.repositories.user_repository_interface import IUserRepository
from .confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class ConfirmUserCreationController:
    def __init__(self, usecase: ConfirmUserCreationUsecase) -> None:
        self.usecase = usecase

    def __call__(self, req: IRequest) -> IResponse:
        try:
            result = self.usecase(
                email=req.data.get('email'),
                confirmation_code=req.data.get('confirmation_code')
            )

            if not result:
                message = "User not found or invalid code."
                return BadRequest(message)

            return OK("User confirmed.")

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
