from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UpdateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo
        self.immutable_fields = ['ra', 'accepted_terms', 'access_level', 'email']
        self.mutable_fields = ['name', 'social_name', 'accepted_notifications', 'certificate_with_social_name', "phone"]

    def __call__(self, mew_user_data: dict, access_token: str) -> User:

        old_user_data = self.repo.check_token(access_token)

        if old_user_data is None:
            raise NoItemsFound("user")

        kvp_to_update = {k: v for k, v in mew_user_data.items() if k in self.mutable_fields and v is not None}

        bool_items = [User.__annotations__[k] for k in self.mutable_fields if User.__annotations__[k] == bool]

        kvp_to_update = {k: eval(v.title()) if User.__annotations__[k] in bool_items and type(v) == str else v for k, v in kvp_to_update.items()}

        for k, v in kvp_to_update.items():
            old_user_data[k] = v

        old_user = User.parse_object(old_user_data)

        new_user = self.repo.update_user(user_email=old_user.email, kvp_to_update=kvp_to_update)

        return new_user

