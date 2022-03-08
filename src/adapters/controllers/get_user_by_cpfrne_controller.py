from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import HttpRequest, HttpResponse, BadRequest, Ok, NoContent, InternalServerError
from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError, NoItemsFound
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.domain.repositories.user_repository_interface import IUserRepository


class GetUserByCpfRneController:

    def __init__(self, userRepository: IUserRepository) -> None:
        self._getAllUserByCpfRneUseCase = GetUserByCpfRneUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is None:
            return BadRequest('Missing parameter.')

        try:
            if not req.query['cpfRne'].isdigit():
                return BadRequest('Invalid parameter.')

            user = await self._getAllUserByCpfRneUseCase(req.query['cpfRne'])
            response = user
            if user is None:
                raise NoItemsFound('')
            return Ok(response)

        except NoItemsFound:
            return NoContent()

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return HttpException(message=err.body, status_code=err.status_code)



