from .get_user_usecase import GetUserUsecase
from .get_user_viewmodel import GetUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError


class GetUserController:

    def __init__(self, usecase: GetUserUsecase):
        self.GetUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('email') is None:
                raise MissingParameters('email')

            user = self.GetUserUsecase(
                email=request.data.get('email')
            )

            viewmodel = GetUserViewmodel(user)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body=err.message)

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:

            return InternalServerError(body=err.args[0])

