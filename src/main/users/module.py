
from typing import Any

from src.modules.change_password.app.change_password_controller import ChangePasswordController
from src.modules.check_token.app.check_token_controller import CheckTokenController
from src.adapters.controllers.confirm_change_password_controller import ConfirmChangePasswordController
from src.adapters.controllers.confirm_user_creation_controller import ConfirmUserCreationController
from src.adapters.controllers.create_user_controller import CreateUserController
from src.adapters.controllers.delete_user_controller import DeleteUserController
from src.modules.get_user.app.get_user_controller import GetUserByCpfRneController
from src.modules.list_users.app.list_users_controller import ListUsersController
from src.modules.login_user.app.login_user_controller import LoginUserController
from src.modules.refresh_token.app.refresh_token_controller import RefreshTokenController
from src.adapters.controllers.resend_creation_confirmation_controller import ResendCreationConfirmationController
from src.adapters.controllers.update_user_controller import UpdateUserController
from src.infra.repositories.cognito_repository import UserRepositoryCognito


class Modular:
    @staticmethod
    def getInject(args: Any):
        for i in Module.getBinds():
            if (i == args or issubclass(i, args)):
                try:
                    inject = (args if i == args else i).__init__.__annotations__
                except AttributeError:
                    return i()

                if len(inject) <= 1:
                    return i()
                else:
                    params = {}
                    for j in range(0, len(inject) - 1):
                        instance = Modular.getInject(list(inject.values())[j])
                        param = list(inject.keys())[j]
                        params[param] = instance
                    return i(**params)
        return None


class Module:

    @staticmethod
    def getBinds():
        return [
            GetUserByCpfRneController,
            CheckTokenController,
            CreateUserController,
            DeleteUserController,
            LoginUserController,
            UpdateUserController,
            RefreshTokenController,
            ChangePasswordController,
            ConfirmChangePasswordController,
            ConfirmUserCreationController,
            UserRepositoryCognito,
            ListUsersController,
            ResendCreationConfirmationController,
            # UserRepositoryMock
        ]
