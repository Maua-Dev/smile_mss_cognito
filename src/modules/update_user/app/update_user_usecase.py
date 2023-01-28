from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UpdateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo
        self.immutable_fields = ['ra', 'accepted_terms', 'access_level', 'email']
        self.mutable_fields = ['name', 'social_name', 'accepted_notifications', 'certificate_with_social_name']

    def __call__(self, mew_user_data: dict, access_token: str) -> User:

        old_user_data = self.repo.check_token(access_token)

        if old_user_data is None:
            raise NoItemsFound("user")

        old_user = User.parse_object(old_user_data)

        for field in self.mutable_fields:
            if field in mew_user_data:
                if field == 'name':
                    setattr(old_user, field, mew_user_data[field].title())
                else:
                    setattr(old_user, field, mew_user_data[field])

        new_user = self.repo.update_user(old_user)

        return new_user

