from .update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction, InvalidTokenError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden
from .update_user_viewmodel import UpdateUserViewmodel


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('access_token')
            access_token = token[1]

            user_data = {
                "name": request.data.get('name'),
                "social_name": request.data.get('social_name'),
                "certificate_with_social_name": request.data.get('certificate_with_social_name'),
                "accepted_notifications": request.data.get('accepted_notifications')
            }

            user = self.UpdateUserUsecase(
                mew_user_data=user_data,
                access_token=access_token
            )

            viewmodel = UpdateUserViewmodel(user)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body='Nenhum usuário econtrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except InvalidTokenError as err:

            return BadRequest(body=f"Token inválido: {err.message}")

        except ForbiddenAction as err:

            return Forbidden(body=f"Ação não permitida: {err.message}")

        except Exception as err:

            return InternalServerError(body=err.args[0])
