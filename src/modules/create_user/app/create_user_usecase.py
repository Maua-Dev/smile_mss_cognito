from src.shared.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import InvalidAdminError, InvalidProfessorError, InvalidStudentError, \
    TermsNotAcceptedError


class CreateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user: User) -> User:

        if user.access_level != ACCESS_LEVEL.USER:
            raise EntityError('access_level')

        if user.role == ROLE.PROFESSOR and User.validate_email_maua_professor(user.email):
            raise InvalidProfessorError('email')

        if user.role == ROLE.STUDENT and not User.validate_ra(user.ra):
            raise InvalidStudentError('ra')

        if user.role == ROLE.ADMIN:
            raise InvalidAdminError('access_level')

        if user.social_name is None and user.certificate_with_social_name:
            raise EntityError('certificate_with_social_name')

        if not user.accepted_terms:
            raise TermsNotAcceptedError('accepted_terms')

        user.email = user.email.lower()

        return self.repo.create_user(user)
