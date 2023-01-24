from src.adapters.errors.http_exception import HttpException
from src.adapters.helpers.http_models import BadRequest, HttpRequest, HttpResponse, InternalServerError, Ok
from src.modules.login_user.app.login_user_viewmodel import LoginUserModel
from src.domain.errors.errors import UnexpectedError, EntityError, NonExistentUser, InvalidCredentials, UserNotConfirmed
from src.domain.repositories.user_repository_interface import IUserRepository
from src.modules.login_user.app.login_user_usecase import LoginUserUsecase


class LoginUserController:
    def __init__(self, userRepository: IUserRepository) -> None:
        self._loginUserUsecase = LoginUserUsecase(userRepository)

    async def __call__(self, req: HttpRequest) -> HttpResponse:

        if req.query is not None:
            return BadRequest('No parameters allowed.')
        if not {'login', 'password'}.issubset(set(req.body)):
            return BadRequest('Missing login and/or password.')

        try:
            cleanLogin = req.body['login'].replace(' ', '')
            data = await self._loginUserUsecase(cleanLogin, req.body["password"])
            loginUserModel = LoginUserModel.fromDict(data=data)
            return Ok(loginUserModel.toDict())

        except InvalidCredentials as e:
            return BadRequest(e.message)

        except NonExistentUser as e:
            return BadRequest(e.message)

        except KeyError as e:
            return BadRequest('Missing parameter: ' + e.args[0])

        except UnexpectedError as e:
            err = InternalServerError(e.message)
            return err

        except UserNotConfirmed as e:
            err = BadRequest(e.message)
            err.status_code = 401
            return err

        except Exception as e:
            err = InternalServerError(e.args[0])
            return err
