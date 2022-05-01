from src.adapters.helpers.http_models import HttpResponse, HttpRequest, BadRequest, Ok, InternalServerError
from src.adapters.viewmodels.list_users_model import ListUsersModel
from src.domain.errors.errors import NonExistentUser
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.list_users_usecase import ListUsersUsecase


class ListUsersController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._listUsersUsecase = ListUsersUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.headers is None:
            return BadRequest('Missing authentication header.')
        if req.body is None:
            return BadRequest('Missing body.')

        try:
            token = req.headers["Authorization"].split(' ')
            if token[0] != 'Bearer':
                return BadRequest('Invalid token.')

            users = await self._listUsersUsecase(req.body, token[1])
            usersModel = ListUsersModel(users)
            return Ok(usersModel.toDict())

        except NonExistentUser as e:
            return BadRequest(e.message)

        except Exception as e:
            return InternalServerError(e.args[0])