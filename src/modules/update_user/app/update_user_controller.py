import json
from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from .update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction, InvalidTokenError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError, Forbidden
from .update_user_viewmodel import UpdateUserViewmodel


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase, observability: IObservability):
        self.UpdateUserUsecase = usecase
        self.mutable_fields = ['name', 'social_name', 'accepted_notifications_sms', 'accepted_notifications_email', 'certificate_with_social_name']
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            
            if request.data.get('Authorization') is None:
                raise MissingParameters('Authorization header')

            token = request.data.get('Authorization').split(' ')

            if len(token) != 2 or token[0] != 'Bearer':
                raise EntityError('access_token')
            access_token = token[1]

            user_data = {k: v for k, v in request.data.items() if k in self.mutable_fields}

            phone = request.data.get("phone") if request.data.get("phone") != "" else None

            if phone is not None:
                phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
                phone = phone if phone.startswith('+') else f'+{phone}'
                user_data["phone"] = phone
                user_data["phone"] = None

                if User.validate_phone(phone) is False:
                    raise EntityError('phone')

            if "accepted_notifications_sms" in user_data:
                user_data["accepted_notifications_sms"] = str(False)

            user = self.UpdateUserUsecase(
                mew_user_data=user_data,
                access_token=access_token
            )

            viewmodel = UpdateUserViewmodel(user)
            response = OK(viewmodel.to_dict())

            self.observability.log_controller_out(input=json.dumps(response.body))
            return response

        except NoItemsFound as err:
            self.observability.log_exception(status_code=404, exception_name="NoItemsFound", message=err.message)

            return NotFound(body='Nenhum usuário encontrado' if err.message == "user" else f"Nenhum usuário encontrado com parâmetro: {err.message}")

        except MissingParameters as err:
            self.observability.log_exception(status_code=400, exception_name="MissingParameters", message=err.message)

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:
            self.observability.log_exception(status_code=400, exception_name="EntityError", message=err.message)

            if "phone" in err.message:
                return BadRequest(body=f"Número de telefone inválido")

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except InvalidTokenError as err:
            self.observability.log_exception(status_code=400, exception_name="InvalidTokenError", message=err.message)
            return BadRequest(body=f"Token inválido: {err.message}")

        except ForbiddenAction as err:
            self.observability.log_exception(status_code=403, exception_name="ForbiddenAction", message=err.message)
            return Forbidden(body=f"Ação não permitida: {err.message}")

        except Exception as err:
            self.observability.log_exception(status_code=500, exception_name=type(err).__name__, message=err.args[0])

            return InternalServerError(body=err.args[0])
