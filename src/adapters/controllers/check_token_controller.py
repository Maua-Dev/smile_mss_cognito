import botocore.errorfactory
from pydantic import ValidationError
import boto3

from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok
from src.adapters.viewmodels.check_token_model import CheckTokenModel
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

        try:
            token = req.headers.get('Authorization').split(' ')
            if len(token) != 2 or token[0] != 'Bearer':
                return BadRequest('Invalid token.')
            access_token = token[1]
            data = await self._checkTokenUsecase(access_token)
            data["validToken"] = True
            checkTokenModel = CheckTokenModel.fromDict(data)
            return Ok(checkTokenModel.toDict())

        except (InvalidToken, UnexpectedError) as e:
            return BadRequest({
                'validToken': False,
                'errorMessage': e.args[0]
                })

        except Exception as e:
            return BadRequest({
                'validToken': False,
                'errorMessage': e.args[0]
            })
