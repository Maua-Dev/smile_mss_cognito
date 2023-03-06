from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:
    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
                'email': 'vitor@gmail.com',
                'name': 'Vitor Soller',
                'password': '123456',
                'ra': '21014442',
                'role': 'STUDENT',
                'access_level': 'USER',
                'accepted_terms': True,
                'accepted_notifications_sms': False,
                'accepted_notifications_email': True,
                'certificate_with_social_name': False,
                'phone': '+5511991758098'
            })

        response = controller(request)

        assert response.status_code == 201
        assert response.body['user']['user_id'] == '00000000000000000000000000000000000' + str(len(repo.users))
        assert response.body['user']['name'] == 'Vitor Soller'
        assert response.body['user']['email'] == 'vitor@gmail.com'
        assert response.body['user']['ra'] == '21014442'
        assert response.body['user']['role'] == 'STUDENT'
        assert response.body['user']['access_level'] == 'USER'
        assert response.body['user']['social_name'] == None
        assert response.body['user']['phone'] == '+5511991758098'
        assert response.body['message'] == 'the user was created'

    def test_create_user_controller_no_plus_in_phone(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '5511991758098'
        })

        response = controller(request)

        assert response.status_code == 201
        assert response.body['user']['user_id'] == '00000000000000000000000000000000000' + str(len(repo.users))
        assert response.body['user']['name'] == 'Vitor Soller'
        assert response.body['user']['email'] == 'vitor@gmail.com'
        assert response.body['user']['ra'] == '21014442'
        assert response.body['user']['role'] == 'STUDENT'
        assert response.body['user']['access_level'] == 'USER'
        assert response.body['user']['social_name'] == None
        assert response.body['user']['phone'] == '+5511991758098'
        assert response.body['message'] == 'the user was created'

    def test_create_user_controller_missing_access_level(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: access_level'

    def test_create_user_controller_invalid_role(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDANT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: role'

    def test_create_user_controller_invalid_access_level(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'INVALIO',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: access_level'

    def test_create_user_controller_missing_role(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: role'

    def test_create_user_controller_missing_accepted_terms(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: accepted_terms'

    def test_create_user_controller_missing_accepted_notifications_sms(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: accepted_notifications_sms'

    def test_create_user_controller_missing_accepted_notifications_email(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'name': 'Vitor Soller',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: accepted_notifications_email'


    def test_create_user_controller_missing_name(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'email': 'vitor@gmail.com',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: name'

    def test_create_user_controller_missing_email(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)

        controller = CreateUserController(usease)

        request = HttpRequest(body={
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

    def test_create_user_controller_missing_password(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'name': "Vitor sOLLER",
            'email': 'vitor@gmail.com',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': False,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: password'

    def test_create_user_controller_wrong_access_level(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'name': 'Vitor Soller',
            'email': 'vitor@gmail.com',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'ADMIN',
            'accepted_terms': True,
            'accepted_notifications_sms': True,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro inválido: access_level'

    def test_create_user_controller_duplicated_item(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'name': 'Vitor Soller',
            'email': 'vitor@maua.br',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'USER',
            'accepted_terms': True,
            'accepted_notifications_sms': True,
            'accepted_notifications_email': True,
            'certificate_with_social_name': False,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 409
        assert response.body == 'Usuário ja cadastrado com esses dados: vitor@maua.br'

    def test_create_user_controller_missing_certificate(self):
        repo = UserRepositoryMock()
        usease = CreateUserUsecase(repo)
        controller = CreateUserController(usease)
        request = HttpRequest(body={
            'name': 'Vitor Soller',
            'email': 'vitor@gmail.com',
            'password': '123456',
            'ra': '21014442',
            'role': 'STUDENT',
            'access_level': 'ADMIN',
            'accepted_terms': True,
            'accepted_notifications_sms': True,
            'accepted_notifications_email': True,
            'phone': '+5511991758098'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: certificate_with_social_name'
