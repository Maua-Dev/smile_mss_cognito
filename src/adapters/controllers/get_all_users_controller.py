from src.adapters.errors.http_exception import HttpException
from src.adapters.viewmodels.get_user_model import GetUserModel
from src.domain.errors.errors import UnexpectedError, NoItemsFound
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.usecases.get_all_users_usecase import GetAllUsersUsecase
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok, NoContent


class GetAllUsersController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._getAllUsersUsecase = GetAllUsersUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')

        try:
            users, count = await self._getAllUsersUsecase()
            cleanUsers = list(map(lambda user: GetUserModel.parse_obj(user), users))
            response = {"users": cleanUsers, "count": count}
            return Ok(response)

        except NoItemsFound:
            return NoContent()

        except (UnexpectedError, Exception) as e:
            err = InternalServerError(e.args[0])
            return HttpException(message=err.body, status_code=err.status_code)