from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidTokenError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, OK, InvalidToken, Unauthorized
from .check_token_viewmodel import CheckTokenViewmodel
from .check_token_usecase import CheckTokenUsecase


class CheckTokenController:
    def __init__(self, usecase: CheckTokenUsecase) -> None:
        self.checkTokenUsecase = usecase

    def __call__(self, req: IRequest) -> IResponse:
        try:
            token = req.headers.get('Authorization').split(' ')
            if len(token) != 2 or token[0] != 'Bearer':
                return BadRequest('Invalid token.')
            access_token = token[1]
            data = self.checkTokenUsecase(access_token)
            data["valid_token"] = True
            check_token_model = CheckTokenViewmodel.from_dict(data)
            return OK(check_token_model.to_dict())

        except ForbiddenAction as e:
            return BadRequest({
                'valid_token': False,
                'error_message': e.args[0]
            })

        except InvalidTokenError as e:

            return Unauthorized("Token inválido ou expirado")

        except Exception as e:
            return BadRequest({
                'valid_token': False,
                'error_message': f"Parâmetro inválido: {e.args[0]}"
            })
