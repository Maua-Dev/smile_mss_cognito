from src.modules.list_professors.app.list_professor_viewmodel import ListProfessorsViewmodel
from src.modules.list_professors.app.list_professors_usecase import ListProfessorsUsecase
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

observability = ObservabilityMock(module_name="list_professors")

class Test_ListProfessorsViewmodel:
    def test_list_professors(self):
        repo = UserRepositoryMock()
        usecase = ListProfessorsUsecase(repo, observability=observability)
        professors = usecase()

        viewmodel = ListProfessorsViewmodel(professors)

        expecetd = {
            'professors': [
                {
                    'user_id': '000000000000000000000000000000000004',
                    'name': 'Vitor Toledo',
                    'email': 'professorvitor@gmail.com',
                    'ra': None,
                    'role': 'PROFESSOR',
                    'access_level': 'USER',
                    'social_name': None,
                    'phone': '+5511991758098'
                }
            ],
            'message': 'the professors were retrieved'
        }

        assert viewmodel.to_dict() == expecetd
