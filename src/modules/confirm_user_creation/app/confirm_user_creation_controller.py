from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok, \
    RedirectResponse, NotFound
from src.modules.change_password.app.change_password_viewmodel import ChangePasswordModel
from src.modules.login_user.app.login_user_viewmodel import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials, \
    UserAlreadyConfirmed
from src.domain.repositories.user_repository_interface import IUserRepository
from src.modules.change_password.app.change_password_usecase import ChangePasswordUsecase
from src.modules.confirm_change_password.app.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.modules.confirm_user_creation.app.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.modules.login_user.app.login_user_usecase import LoginUserUsecase


class ConfirmUserCreationController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._confirmUserCreationUsecase = ConfirmUserCreationUsecase(
            userRepository)

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

        except NonExistentUser as e:
            err = NotFound(e.message)
            return err

        except UserAlreadyConfirmed as e:
            return RedirectResponse({
                "message": e.message
            }
            )

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
