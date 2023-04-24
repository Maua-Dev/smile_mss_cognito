import json
from src.shared.domain.observability.observability_interface import IObservability
from .login_user_usecase import LoginUserUsecase
from .login_user_viewmodel import LoginUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction, InvalidCredentials, UserNotConfirmed
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import NotFound, BadRequest, InternalServerError, OK, Forbidden, \
    Unauthorized


class LoginUserController:

    def __init__(self, usecase: LoginUserUsecase, observability: IObservability):
        self.loginUserUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('login') is None:
                raise MissingParameters('login')

            if request.data.get('password') is None:
                raise MissingParameters('password')

            clean_login = request.body['login'].replace(' ', '')
            data = self.loginUserUsecase(clean_login, request.body["password"])
            login_user_viewmodel = LoginUserViewmodel(data)
            response = OK(login_user_viewmodel.to_dict())

            self.observability.log_controller_out(input=json.dumps(response.body))
            
            
            return response

        except NoItemsFound as err:
            self.observability.log_exception(status_code=404, exception_name="NoItemsFound", message=err.message)

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)
            return Forbidden(body=f"Ação não permitida: {err.message}")

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except InvalidCredentials as err:
            self.observability.log_exception(status_code=403, exception_name="InvalidCredentials", message=err.message)
            return Forbidden(body="Usuário ou senha inválidos")

        except UserNotConfirmed as err:
            self.observability.log_exception(status_code=401, exception_name="UserNotConfirmed", message=err.message)
            return Unauthorized(body="Usuário não confirmado")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])

