from .login_user_usecase import LoginUserUsecase
from .login_user_viewmodel import LoginUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import NotFound, BadRequest, InternalServerError, OK, Forbidden


class LoginUserController:

    def __init__(self, usecase: LoginUserUsecase):
        self.loginUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('login') is None:
                raise MissingParameters('login')

            if request.data.get('password') is None:
                raise MissingParameters('password')

            clean_login = request.body['login'].replace(' ', '')
            data = self.loginUserUsecase(clean_login, request.body["password"])
            login_user_viewmodel = LoginUserViewmodel(data)
            return OK(login_user_viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except ForbiddenAction as err:

            return Forbidden(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:

            return InternalServerError(body=err.args[0])

