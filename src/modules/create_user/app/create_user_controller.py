from pydantic import ValidationError

from src.adapters.errors.http_exception import HttpException
from src.domain.entities.user import User
from src.domain.errors.errors import UnexpectedError, NoItemsFound, EntityError, InvalidCredentials, UserAlreadyExists, \
    IncompleteUser
from src.domain.repositories.user_repository_interface import IUserRepository
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok, NoContent


class CreateUserController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._createUserUsecase = CreateUserUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if req.body is None:
            return BadRequest('Missing body.')

        try:
            req.body['cpfRne'] = req.body.get('cpf_rne').replace('.', '').replace(
                '-', '').replace(' ', '') if req.body.get('cpf_rne') else None
            req.body['accessLevel'] = req.body.get('access_level')
            req.body['acceptedTerms'] = req.body.get('accepted_terms')
            req.body['acceptedNotifications'] = req.body.get(
                'accepted_notifications')
            req.body['socialName'] = req.body.get('social_name')
            req.body['email'] = req.body.get('email').replace(
                ' ', '') if req.body.get('email') else None

            # removes keys that have no value
            req.body = {k: v for k, v in req.body.items() if v is not None}

            user = User.parse_obj(req.body)
            await self._createUserUsecase(user)
            response = {f"User {user.name} created."}
            return Ok(response)

        except EntityError as e:
            return BadRequest(e.message)

        except ValidationError:
            return BadRequest("Invalid parameters.")

        except InvalidCredentials as e:
            return BadRequest(e.message)

        except UserAlreadyExists as e:
            return BadRequest(e.message)

        except IncompleteUser as e:
            return BadRequest(e.message)

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
