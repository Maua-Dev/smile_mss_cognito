from pydantic import ValidationError

from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok, \
    RedirectResponse, NotFound
from src.adapters.viewmodels.change_password_model import ChangePasswordModel
from src.adapters.viewmodels.login_user_model import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials, \
    UserAlreadyConfirmed
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.change_password_usecase import ChangePasswordUsecase
from src.domain.usecases.confirm_change_password_usecase import ConfirmChangePasswordUsecase
from src.domain.usecases.confirm_user_creation_usecase import ConfirmUserCreationUsecase
from src.domain.usecases.login_user_usecase import LoginUserUsecase
from src.domain.usecases.resend_creation_confirmation_usecase import ResendCreationConfirmationUsecase


class ResendCreationConfirmationController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._resendCreationConfirmationUsecase = ResendCreationConfirmationUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if not {'cpf_rne'}.issubset(set(req.body)):
            return BadRequest('Missing login or code.')

        try:

            req.body['cpfRne'] = req.body['cpf_rne']

            result = await self._resendCreationConfirmationUsecase(cpfRne=str(req.body['cpfRne']))

            if not result:
                message = "Something with the request went wrong."
                return BadRequest(message)

            return Ok("New email sent.")

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except NonExistentUser as e:
            err = NotFound(e.message)
            return err

        except EntityError as e:
            return BadRequest(e.message)

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
