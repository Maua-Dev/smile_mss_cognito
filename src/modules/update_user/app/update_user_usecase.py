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

        old_user = User.parse_object(old_user_data)

        for field in self.mutable_fields:
            if field in mew_user_data and mew_user_data.get(field) is not None:
                if field in ["name", "social_name"]:
                    setattr(old_user, field, mew_user_data[field].title())
                else:
                    setattr(old_user, field, mew_user_data[field])

        new_user = self.repo.update_user(user_email=old_user.email, kvp_to_update={field: getattr(old_user, field) for field in self.mutable_fields})

        return new_user

