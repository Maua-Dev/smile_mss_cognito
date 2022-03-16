from pydantic import ValidationError

from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok
from src.adapters.viewmodels.change_password_model import ChangePasswordModel
from src.adapters.viewmodels.login_user_model import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.change_password_usecase import ChangePasswordUsecase
from src.domain.usecases.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.domain.usecases.login_user_usecase import LoginUserUsecase


class ConfirmChangePasswordController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._confirmChangePasswordUsecase = ConfirmChangePasswordUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if not {'login', 'new_password', 'confirmation_code'}.issubset(set(req.body)):
            return BadRequest('Missing login, new password or confirmation code.')

        try:
            result = await self._confirmChangePasswordUsecase(
                login=str(req.body['login']),
                newPassword=str(req.body['new_password']),
                code=str(req.body['confirmation_code'])
            )

            changePasswordModel = ChangePasswordModel(result=result)
            if not result:
                changePasswordModel.message = "User not found, invalid confirmation code or weak new password."
                return BadRequest(changePasswordModel.toDict())

            return Ok(changePasswordModel.toDict())

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
