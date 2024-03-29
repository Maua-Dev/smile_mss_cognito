import abc
from datetime import datetime
import re

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.helpers.errors.domain_errors import EntityError


class User(abc.ABC):
    user_id: str
    email: str
    name: str
    password: str
    ra: str
    role: ROLE
    access_level: ACCESS_LEVEL
    created_at: int  # milliseconds
    updated_at: int  # milliseconds
    social_name: str
    accepted_terms: bool
    accepted_notifications_sms: bool
    accepted_notifications_email: bool
    certificate_with_social_name: bool
    phone: str #with country code
    MIN_NAME_LENGTH = 2
    USER_ID_LENGTH = 36

    def __init__(self, user_id: str, email: str, name: str, password: str, ra: str, role: ROLE, access_level: ACCESS_LEVEL,
                 created_at: int, updated_at: int, social_name: str, accepted_terms: bool, accepted_notifications_sms: bool,
                 certificate_with_social_name: bool, phone: str, accepted_notifications_email: bool):

        if user_id is not None:
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

        if accepted_notifications_sms is not None:
            if type(accepted_notifications_sms) != bool:
                raise EntityError("accepted_notifications_sms")
        self.accepted_notifications_sms = accepted_notifications_sms
        
        if accepted_notifications_email is not None:
            if type(accepted_notifications_email) != bool:
                raise EntityError("accepted_notifications_email")
        self.accepted_notifications_email = accepted_notifications_email

        if certificate_with_social_name is not None:
            if type(certificate_with_social_name) != bool:
                raise EntityError("certificate_with_social_name")
        self.certificate_with_social_name = certificate_with_social_name

        if phone is not None:
            if not User.validate_phone(phone):
                raise EntityError("phone")
        self.phone = phone

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
        name_regex = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')
        return bool(re.fullmatch(name_regex, name))

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
        elif not ra.isdecimal():
            return False

        return True

    @staticmethod
    def validate_phone(phone: str) -> bool:
        if type(phone) != str:
            return False
        elif phone[0] != "+":
            return False
        elif phone[1:].isdecimal() is False:
            return False

        return True

    @staticmethod
    def validate_email_maua_professor(email: str) -> bool:
        if email == None:
            return False

        regex = re.compile(
            r"^(?!\d{2}\.\d{5}-\d)[\w.-]+@maua\.br$")

        return bool(re.fullmatch(regex, email))

    @staticmethod
    def parse_object(user: dict) -> 'User':
        return User(
            user_id=user.get("user_id"),
            email=user['email'],
            name=user['name'].title(),
            password=user['password'] if user.get('password') is not None else None,
            ra=user['ra'] if 'ra' in user else None,
            role=ROLE[user['role']],
            access_level=ACCESS_LEVEL[user['access_level']],
            created_at=user['created_at'] if user.get('created_at') is not None else None,
            updated_at=user['updated_at'] if user.get('updated_at') is not None else None,
            social_name=user['social_name'].title() if user.get('social_name') is not None else None,
            accepted_terms=user['accepted_terms'] if user.get('accepted_terms') is not None else None,
            accepted_notifications_sms=user['accepted_notifications_sms'] if user.get(
                'accepted_notifications_sms') is not None else None,
            certificate_with_social_name=user['certificate_with_social_name'] if user.get(
                'certificate_with_social_name') is not None else None,
            phone=user['phone'] if user.get('phone') is not None else None,
            accepted_notifications_email=user['accepted_notifications_email'] if user.get('accepted_notifications_email') is not None else None
        )

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'password': self.password,
            'ra': self.ra,
            'role': self.role.value,
            'access_level': self.access_level.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'social_name': self.social_name,
            'accepted_terms': self.accepted_terms,
            'accepted_notifications_sms': self.accepted_notifications_sms,
            'accepted_notifications_email': self.accepted_notifications_email,
            'certificate_with_social_name': self.certificate_with_social_name,
            'phone': self.phone
        }
