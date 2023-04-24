from src.shared.domain.entities.user import User
from src.shared.domain.observability.observability_interface import IObservability
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UpdateUserUsecase:

    def __init__(self, repo: IUserRepository, observability: IObservability):
        self.repo = repo
        self.immutable_fields = ['ra', 'accepted_terms', 'access_level', 'email']
        self.mutable_fields = ['name', 'social_name', 'accepted_notifications_sms', 'accepted_notifications_email', 'certificate_with_social_name', "phone"]
        self.observability = observability

    def __call__(self, mew_user_data: dict, access_token: str) -> User:
        self.observability.log_usecase_in()

        old_user_data = self.repo.check_token(access_token)

        if old_user_data is None:
            raise NoItemsFound("user")

        kvp_to_update = {k: v for k, v in mew_user_data.items() if k in self.mutable_fields and v is not None}

        bool_items = [User.__annotations__[k] for k in self.mutable_fields if User.__annotations__[k] == bool]

        kvp_to_update = {k: eval(v.title()) if User.__annotations__[k] in bool_items and type(v) == str else v for k, v in kvp_to_update.items()}

        for k, v in kvp_to_update.items():
            old_user_data[k] = v if v != "" else None

        old_user = User.parse_object(old_user_data)

        kvp_to_update = {k: str(v) for k, v in kvp_to_update.items()}

        kvp_to_update['phone'] = None


        new_user = self.repo.update_user(user_email=old_user.email, kvp_to_update=kvp_to_update)
        self.observability.log_usecase_out()

        return new_user

