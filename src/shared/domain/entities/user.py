import abc
from datetime import datetime
from typing import List
import re

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.errors.errors import EntityError


class User(abc.ABC):
    user_id: str
    email: str
    name: str
    password: str
    ra: str
    role: ROLE
    access_level: ACCESS_LEVEL
    created_at: int  # microsseconds
    updated_at: int  # microsseconds
    social_name: str
    accepted_terms: bool
    accepted_notifications: bool
    certificate_with_social_name: bool
    MIN_NAME_LENGTH = 2
    USER_ID_LENGTH = 4

    def __init__(self, user_id: str, email: str, name: str, password: str,
                 ra: str, role: ROLE, access_level: ACCESS_LEVEL, created_at: datetime,
                 updated_at: datetime, social_name: str, accepted_terms: bool,
                 accepted_notifications: bool, certificate_with_social_name: bool
                 ):
        if not User.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name.title()

        if password is not None:
            if not User.validate_password(password):
                raise EntityError("password")
        self.password = password

        if ra is not None:
            if not User.validate_ra(ra):
                raise EntityError("ra")
        self.ra = ra

        if type(role) != ROLE:
            raise EntityError("role")
        self.role = role

        if type(access_level) != ACCESS_LEVEL:
            raise EntityError("access_level")
        self.access_level = access_level

        if created_at is not None:
            if type(created_at) != int:
                raise EntityError("created_at")
        self.created_at = created_at

        if updated_at is not None:
            if type(updated_at) != int:
                raise EntityError("updated_at")
        self.updated_at = updated_at

        if social_name is not None:
            if not User.validate_name(social_name):
                raise EntityError("social_name")
            self.social_name = social_name.title()
        else:
            self.social_name = social_name

        if accepted_terms is not None:
            if type(accepted_terms) != bool:
                raise EntityError("accepted_terms")
        self.accepted_terms = accepted_terms

        if accepted_notifications is not None:
            if type(accepted_notifications) != bool:
                raise EntityError("accepted_notifications")
        self.accepted_notifications = accepted_notifications

        if certificate_with_social_name is not None:
            if type(certificate_with_social_name) != bool:
                raise EntityError("certificate_with_social_name")
        self.certificate_with_social_name = certificate_with_social_name

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        if type(user_id) != str:
            return False
        if len(user_id) != User.USER_ID_LENGTH:
            return False
        return True

    def __repr__(self):
        return f"User(name={self.name}, role={self.role.value}, user_id={self.user_id})"

    def __eq__(self, other):
        return self.name == other.name and self.role == other.role and self.user_id == other.user_id

    @staticmethod
    def validate_email(email) -> bool:
        if email == None:
            return False

        regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        return bool(re.fullmatch(regex, email))

    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        elif type(name) != str:
            return False
        elif len(name) < User.MIN_NAME_LENGTH:
            return False

        return True

    @staticmethod
    def validate_password(name: str) -> bool:
        if type(name) != str:
            return False

        return True

    @staticmethod
    def validate_ra(ra: str) -> bool:
        if type(ra) != str:
            return False
        elif len(ra) != 8:
            return False

        return True

    def dict(self):
        return self.__dict__
