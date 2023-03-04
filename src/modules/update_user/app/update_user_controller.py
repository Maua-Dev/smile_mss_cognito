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
        self.mutable_fields = ['name', 'social_name', 'accepted_notifications_sms', 'accepted_notifications_email', 'certificate_with_social_name', "phone"]

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('access_token')
            access_token = token[1]

            user_data = {k: v for k, v in request.data.items() if k in self.mutable_fields}

            user = self.UpdateUserUsecase(
                mew_user_data=user_data,
                access_token=access_token
            )

            viewmodel = UpdateUserViewmodel(user)

            return OK(viewmodel.to_dict())

        except NoItemsFound as err:

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

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
