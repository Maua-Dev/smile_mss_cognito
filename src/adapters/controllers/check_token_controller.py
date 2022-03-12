from pydantic import ValidationError

from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok
from src.adapters.viewmodels.login_user_model import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials, InvalidToken
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.check_token_usecase import CheckTokenUsecase
from src.domain.usecases.login_user_usecase import LoginUserUsecase


class CheckTokenController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._checkTokenUsecase = CheckTokenUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if req.body is None:
            return BadRequest('Missing body.')

        try:
            token_validated = await self._checkTokenUsecase(req.body["cpfRne"], req.body["token"])
            response = {"tokenValidated": True}
            return Ok(response)

        except InvalidToken:
            return BadRequest({"tokenValidated": False})

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except (UnexpectedError, Exception) as e:
            err = InternalServerError(e.message)
            return HttpException(message=err.body, status_code=err.status_code)