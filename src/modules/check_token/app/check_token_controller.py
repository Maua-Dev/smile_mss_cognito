import botocore.errorfactory
import boto3

from src.shared.errors.http_exception import HttpException
from src.shared.helpers.external_interfaces.http_models import HttpRequest, HttpResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, OK
from src.modules.check_token.app.check_token_viewmodel import CheckTokenModel
from src.modules.login_user.app.login_user_viewmodel import LoginUserModel
from src.shared.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials, InvalidToken
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.modules.check_token.app.check_token_usecase import CheckTokenUsecase
from src.modules.login_user.app.login_user_usecase import LoginUserUsecase


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
