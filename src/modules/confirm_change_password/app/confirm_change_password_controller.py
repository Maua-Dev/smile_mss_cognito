from .confirm_change_password_usecase import ConfirmChangePasswordUsecase
from .confirm_change_password_viewmodel import ConfirmChangePasswordViewmodel

from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class ConfirmChangePasswordController:
    def __init__(self, usecase: ConfirmChangePasswordUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')
            if request.data.get('new_password') is None:
                raise MissingParameters('new_password')
            if request.data.get('confirmation_code') is None:
                raise MissingParameters('confirmation_code')

            resp = self.usecase(
                email=request.data.get('email'),
                confirmation_code=request.data.get('confirmation_code'),
                new_password=request.data.get('new_password')
            )

            viewmodel = ConfirmChangePasswordViewmodel(resp)

            if not resp:
                viewmodel.message = "User not found, invalid confirmation code or weak new password."
                return BadRequest(viewmodel.to_dict())

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
