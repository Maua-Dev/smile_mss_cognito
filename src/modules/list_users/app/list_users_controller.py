from .list_users_usecase import ListUsersUsecase
from .list_users_viewmodel import ListUsersViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden


class ListUsersController:

    def __init__(self, usecase: ListUsersUsecase):
        self.ListUsersUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('access_token')
            access_token = token[1]

            if request.data.get('user_list') is None:
                raise MissingParameters('user_list')

            user_list = self.ListUsersUsecase(
                user_list=request.data.get('user_list'),
                access_token=access_token
            )

            viewmodel = ListUsersViewmodel(user_list)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:

            return Forbidden(body=err.message)

        except EntityError as err:

            return BadRequest(body=f'Parâmetro inválido: {err.message}')

        except Exception as err:

            return InternalServerError(body=err.args[0])

