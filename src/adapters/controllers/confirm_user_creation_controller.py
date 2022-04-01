from pydantic import ValidationError

from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok
from src.adapters.viewmodels.change_password_model import ChangePasswordModel
from src.adapters.viewmodels.login_user_model import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.change_password_usecase import ChangePasswordUsecase
from src.domain.usecases.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.domain.usecases.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.domain.usecases.login_user_usecase import LoginUserUsecase


class ConfirmUserCreationController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._confirmUserCreationUsecase = ConfirmUserCreationUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if not {'login', 'code'}.issubset(set(req.body)):
            return BadRequest('Missing login or code.')

        try:
            result = await self._confirmUserCreationUsecase(
                login=str(req.body['login']),
                code=str(req.body['code'])
            )

            if not result:
                message = "User not found or invalid code."
                return BadRequest(message)

            return Ok("User confirmed.")

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
