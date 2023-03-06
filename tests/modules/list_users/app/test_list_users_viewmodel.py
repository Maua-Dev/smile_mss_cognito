from src.modules.list_users.app.list_users_usecase import ListUsersUsecase
from src.modules.list_users.app.list_users_viewmodel import ListUsersViewmodel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersViewmodel:

    def test_list_users_viewmodel(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        user_list_dict_list = usecase(user_list=[repo.confirmed_users[0].user_id],
                                      access_token="valid_access_token-vitor@maua.br")

        viewmodel = ListUsersViewmodel(user_list_dict_list)

        expected = {
            'user_list': {
                '000000000000000000000000000000000001': {
                    'user_id': '000000000000000000000000000000000001',
                    'name': 'Caio Soller',
                    'email': 'zeeba@gmail.com',
                    'ra': '20014309',
                    'role': 'STUDENT',
                    'access_level': 'USER',
                    'social_name': 'Zeeba Toledo',
                    "phone": "+5511999451100",
                }
            },
            'message': 'the users were retrieved'
        }

        assert viewmodel.to_dict() == expected

    def test_list_users_viewmodel_more_users(self):
        repo = UserRepositoryMock()
        usecase = ListUsersUsecase(repo)

        user1 = repo.confirmed_users[0]
        user2 = repo.confirmed_users[1]

        user_list_dict_list = usecase(user_list=[user1.user_id, user2.user_id],
                                      access_token="valid_access_token-vitor@maua.br")

        viewmodel = ListUsersViewmodel(user_list_dict_list)

        expected = {
            'user_list': {
                '000000000000000000000000000000000001': {
                    'user_id': '000000000000000000000000000000000001',
                    'name': 'Caio Soller',
                    'email': 'zeeba@gmail.com',
                    'ra': '20014309',
                    'role': 'STUDENT',
                    'access_level': 'USER',
                    'social_name': 'Zeeba Toledo',
                    "phone": "+5511999451100",
                },
                '000000000000000000000000000000000002': {
                    'user_id': '000000000000000000000000000000000002',
                    'name': 'Vitor Branco',
                    'email': 'vitor@maua.br',
                    'ra': '20014309',
                    'role': 'STUDENT',
                    'access_level': 'ADMIN',
                    'social_name': 'Zeeba Toledo',
                    "phone": "+5511991758098",
                }
            },
            'message': 'the users were retrieved'
        }

        assert viewmodel.to_dict() == expected
