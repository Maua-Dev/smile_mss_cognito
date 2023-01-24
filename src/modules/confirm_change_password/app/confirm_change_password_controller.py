from src.shared.errors.http_exception import HttpException
from src.shared.helpers.external_interfaces.http_models import HttpRequest, HttpResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, OK
from src.modules.change_password.app.change_password_viewmodel import ChangePasswordModel
from src.modules.login_user.app.login_user_viewmodel import LoginUserModel
from src.shared.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase
from src.modules.confirm_change_password.app.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.modules.login_user.app.login_user_usecase import LoginUserUsecase


class ConfirmChangePasswordController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._confirmChangePasswordUsecase = ConfirmChangePasswordUsecase(
            userRepository)

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

            return OK(changePasswordModel.toDict())

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
