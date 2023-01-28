from src.shared.domain.entities.enums import ACCESS_LEVEL
from src.shared.domain.entities.user import User

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction


class ListUsersUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_list: list, access_token: str) -> dict:

            user_requester_data = self.repo.check_token(access_token)

            if user_requester_data is None:
                raise NoItemsFound("user")

            user_requester = User.parse_object(user_requester_data)

            if user_requester.access_level != ACCESS_LEVEL.ADMIN:
                raise ForbiddenAction("user")

            if type(user_list) != list:
                raise EntityError("user_list")

            for id in user_list:
                if not User.validate_user_id(id):
                    raise EntityError("user_id")

            all_users = self.repo.get_all_users()
            user_dict_list = {}
            for user in all_users:
                if user.user_id in user_list:
                    user_dict_list[user.user_id] = user

            if len(user_dict_list) != len(user_list):
                for id in user_list:
                    if id not in user_dict_list.keys():
                        raise NoItemsFound(f"user_id: {id}")

            return user_dict_list
