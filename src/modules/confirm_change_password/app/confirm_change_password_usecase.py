from src.shared.domain.repositories.user_repository_interface import IUserRepository


class ConfirmChangePasswordUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, new_password: str, confirmation_code: str) -> bool:

        result = self.repo.confirm_change_password(
            email, new_password, confirmation_code
        )

        if not result:
            pass

        return result
