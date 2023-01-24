from src.adapters.errors.http_exception import HttpException
from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError, NoItemsFound, EntityError, NonExistentUser, InvalidToken
from src.domain.repositories.user_repository_interface import IUserRepository
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok, NoContent
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase


class UpdateUserController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._updateUserUsecase = UpdateUserUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if req.body is None:
            return BadRequest('Missing body.')

        try:
            token = req.headers.get('Authorization').split(' ')
            if len(token) != 2 or token[0] != 'Bearer':
                return BadRequest('Invalid token.')
            accessToken = token[1]

            userData = {
                "name": req.body.get('name'),
                "socialName": req.body.get('social_name'),
                "certificateWithSocialName": req.body.get('certificate_with_social_name'),
            }

            await self._updateUserUsecase(userData, accessToken)
            response = {f"User {userData['name']} updated."}
            return Ok(response)

        except InvalidToken as e:
            return BadRequest(e.message)

        except EntityError as e:
            return BadRequest(e.message)

        # except ValidationError:
        #     return BadRequest("Invalid parameters.")

        except NonExistentUser as e:
            return BadRequest(e.message)

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
