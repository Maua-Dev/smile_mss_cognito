from src.shared.errors.http_exception import HttpException
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_models import HttpRequest, HttpResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, OK
from src.modules.change_password.app.change_password_viewmodel import ChangePasswordModel
from src.modules.login_user.app.login_user_viewmodel import LoginUserModel
from src.shared.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials, UserNotConfirmed
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase
from src.modules.login_user.app.login_user_usecase import LoginUserUsecase


class ChangePasswordController:
    def __init__(self, usecase: ChangePasswordUsecase):
        self._changePasswordUsecase = usecase

    async def __call__(self, req: IRequest) -> IResponse:

        if req.data is not None:
            return BadRequest('No parameters allowed.')
        if not req.data:
            return BadRequest('Missing body.')

        try:
            cleanLogin = str(req.body["login"]).replace(' ', '')
            result = await self._changePasswordUsecase(cleanLogin)
            changePasswordModel = ChangePasswordModel(result=result)
            if not result:
                changePasswordModel.message = "User not found"
                return BadRequest(changePasswordModel.toDict())

            return OK(changePasswordModel.toDict())

        except KeyError as err:
            return BadRequest('Missing parameter: ' + err.args[0])

        except UnexpectedError as err:
            err = InternalServerError(body=err.message)
            return err

        except NonExistentUser as err:
            err = BadRequest(body=err.message + " or is not confirmed")
            return err

        except UserNotConfirmed as err:
            err = BadRequest(body=err.message)
            err.status_code = 401
            return err

        except Exception as err:
            err = InternalServerError(body=err.args[0])
            return err
