from .list_professor_viewmodel import ListProfessorsViewmodel
from .list_professors_usecase import ListProfessorsUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class ListProfessorsController:
    def __init__(self, usecase: ListProfessorsUsecase) -> None:
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:

            list_professor = self.usecase()

            viewmodel = ListProfessorsViewmodel(list_professor)

            return OK(viewmodel.to_dict())

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
