from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import HttpRequest, HttpResponse, BadRequest, Ok, NoContent, InternalServerError
from src.adapters.viewmodels.get_user_model import GetUserModel
from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError, NoItemsFound, NonExistentUser
from src.domain.usecases.get_user_by_cpfrne_usecase import GetUserByCpfRneUsecase
from src.domain.repositories.user_repository_interface import IUserRepository


class GetUserByCpfRneController:

    def __init__(self, userRepository: IUserRepository) -> None:
        self._getAllUserByCpfRneUseCase = GetUserByCpfRneUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is None:
            return BadRequest('Missing parameter.')

        try:
            if  type(req.query['cpfRne']) != int:
                return BadRequest('Invalid parameter. (Cpf value should be Int) ')

            user = await self._getAllUserByCpfRneUseCase(int(req.query['cpfRne']))
            response = GetUserModel.parse_obj(user)

            if user is None:
                raise NonExistentUser('')
            return Ok(response)

        except (NoItemsFound, NonExistentUser):
            return NoContent()

        except (UnexpectedError, Exception) as e:
            err = InternalServerError(e.message)
            return HttpException(message=err.body, status_code=err.status_code)



