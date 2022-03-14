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
        if req.body is None:
            return BadRequest('Missing body.')

        try:
            data = await self._checkTokenUsecase(req.body["access_token"])
            checkTokenModel = CheckTokenModel.fromDict(data)
            return Ok(checkTokenModel.toDict())

        except (InvalidToken, UnexpectedError) as e:
            return BadRequest({
                'tokenValidated': False,
                'errorMessage': e.args[0]
                })

        except Exception as e:
            return BadRequest({
                'tokenValidated': False,
                'errorMessage': e.args[0]
            })
