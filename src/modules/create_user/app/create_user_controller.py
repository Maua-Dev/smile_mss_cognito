import datetime
from .create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.shared.domain.entities.user import User
from .create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Conflict, \
    Created


class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase) -> None:
        self.createUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('access_level') is None:
                raise MissingParameters('access_level')

            if request.data.get('access_level') not in [access_level.value for access_level in ACCESS_LEVEL]:
                raise EntityError('access_level')

            if request.data.get('role') is None:
                raise MissingParameters('role')

            if request.data.get('role') not in [role.value for role in ROLE]:
                raise EntityError('role')

            if request.data.get('accepted_terms') is None:
                raise MissingParameters('accepted_terms')

            if request.data.get('accepted_notifications') is None:
                raise MissingParameters('accepted_notifications')

            if request.data.get('name') is None:
                raise MissingParameters('name')

            if request.data.get('email') is None:
                raise MissingParameters('email')

            if request.data.get('password') is None:
                raise MissingParameters('password')

            if request.data.get('phone') is None:
                raise MissingParameters('phone')

            if request.data.get('certificate_with_social_name') is None:
                raise MissingParameters('certificate_with_social_name')

            user_dict = {
                'email': request.data.get('email').replace(' ', ''),
                'name': request.data.get('name'),
                'password': request.data.get('password'),
                'ra': request.data.get('ra').replace('.', '').replace('-', '').replace(' ', '') if request.data.get('ra') else None,
                'role': request.data.get('role'),
                'access_level': request.data.get('access_level'),
                'created_at': int(datetime.datetime.now().timestamp()*1000),
                'updated_at': None,
                'social_name': request.data.get('social_name') if request.data.get('social_name') else None,
                'accepted_terms': request.data.get('accepted_terms'),
                'accepted_notifications': request.data.get('accepted_notifications'),
                'certificate_with_social_name': request.data.get('certificate_with_social_name'),
                'phone': request.data.get('phone'),
            }

            new_user = User.parse_object(user_dict)
            created_user = self.createUserUsecase(new_user)

            viewmodel = CreateUserViewmodel(created_user)

            return Created(viewmodel.to_dict())

        except DuplicatedItem as err:

            return Conflict(body=f"Usuário ja cadastrado com esses dados: {err.message}")

        except MissingParameters as err:

            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except EntityError as err:

            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except Exception as err:

            return InternalServerError(body=err.args[0])
