from pydantic import ValidationError

from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok
from src.adapters.viewmodels.change_password_model import ChangePasswordModel
from src.adapters.viewmodels.login_user_model import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials, UserNotConfirmed
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.change_password_usecase import ChangePasswordUsecase
from src.domain.usecases.login_user_usecase import LoginUserUsecase


class ChangePasswordController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._changePasswordUsecase = ChangePasswordUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if not req.body:
            return BadRequest('Missing body.')


        try:
            cleanLogin = str(req.body["login"]).replace(' ', '')
            result = await self._changePasswordUsecase(cleanLogin)
            changePasswordModel = ChangePasswordModel(result=result)
            if not result:
                changePasswordModel.message = "User not found"
                return BadRequest(changePasswordModel.toDict())

            return Ok(changePasswordModel.toDict())

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except NonExistentUser as e:
            err = BadRequest(e.message + " or is not confirmed")
            return err

        except UserNotConfirmed as e:
            err = BadRequest(e.message)
            err.status_code = 401
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err