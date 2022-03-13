from pydantic import ValidationError

from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok
from src.adapters.viewmodels.login_user_model import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.login_user_usecase import LoginUserUsecase


class LoginUserController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._loginUserUsecase = LoginUserUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if req.body is None:
            return BadRequest('Missing body.')

        try:
            tokens = await self._loginUserUsecase(req.body["cpfRne"], req.body["password"])
            accessToken, refreshToken = tokens
            loginUserModel = LoginUserModel(accessToken=accessToken, refreshToken=refreshToken)
            return Ok(loginUserModel.toDict())


        except InvalidCredentials as e:
            return BadRequest(e.message)

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err