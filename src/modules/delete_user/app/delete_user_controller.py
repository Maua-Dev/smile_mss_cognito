from src.adapters.helpers.http_models import HttpRequest, HttpResponse, BadRequest, InternalServerError, Ok
from src.domain.errors.errors import NonExistentUser
from src.domain.repositories.user_repository_interface import IUserRepository
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase


class DeleteUserController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._deleteUserUsecase = DeleteUserUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if req.body is None:
            return BadRequest('Missing body.')
        if 'cpfRne' not in req.body:
            return BadRequest('Missing Cpf Rne.')
        try:
            await self._deleteUserUsecase(req.body['cpfRne'])
            return Ok('User deleted.')

        except NonExistentUser as e:
            return BadRequest(e.message)

        except Exception as e:
            return InternalServerError(e.args[0])
