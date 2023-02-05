from enum import Enum
from typing import List

from src.shared.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.shared.domain.entities.user import User


class UserCognitoDTO:
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
    phone: str  # with country code
    # MANDATORY_FIELDS = ["email", "name", "role", "access_level", "phone"]
    # CUSTOM_FIELDS = ["role", "access_level", "ra", "social_name", "accepted_terms", "accepted_notifications", "certificate_with_social_name"]
    TO_COGNITO_DICT = {
        "email": "email",
        "name": "name",
        "role": "custom:role",
        "access_level": "custom:accessLevel",
        "ra": "custom:ra",
        "social_name": "custom:socialName",
        "accepted_terms": "custom:acceptedTerms",
        "accepted_notifications": "custom:acceptedNotific",
        "certificate_with_social_name": "custom:certWithSocialName",
        "phone": "phone_number"
    }
    FROM_COGNITO_DICT = {value: key for key, value in TO_COGNITO_DICT.items()}
    FROM_COGNITO_DICT["sub"] = "user_id"

    def __init__(self, user_id: str, email: str, name: str, role: ROLE, access_level: ACCESS_LEVEL, phone: str, ra: str = None,  created_at: int = None, updated_at: int = None, social_name: str = None, accepted_terms: bool = None, accepted_notifications: bool = None, certificate_with_social_name: bool = None, password: str = None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.ra = ra
        self.role = role
        self.access_level = access_level
        self.created_at = created_at
        self.updated_at = updated_at
        self.social_name = social_name
        self.accepted_terms = accepted_terms
        self.accepted_notifications = accepted_notifications
        self.certificate_with_social_name = certificate_with_social_name
        self.phone = phone

    @staticmethod
    def from_entity(user: User):
        return UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            password=user.password,
            ra=user.ra,
            role=user.role,
            access_level=user.access_level,
            created_at=user.created_at,
            updated_at=user.updated_at,
            social_name=user.social_name,
            accepted_terms=user.accepted_terms,
            accepted_notifications=user.accepted_notifications,
            certificate_with_social_name=user.certificate_with_social_name,
            phone=user.phone
        )

    def to_cognito_attributes(self) -> List[dict]:
        user_attributes = [self.parse_attribute(value=getattr(self, att), name=self.TO_COGNITO_DICT[att]) for att in self.TO_COGNITO_DICT]
        user_attributes = [att for att in user_attributes if att["Value"] != str(None)]

        return user_attributes

    @staticmethod
    def from_cognito(data: dict) -> "UserCognitoDTO":
        user_data = next((value for key, value in data.items() if "Attribute" in key), None)

        user_data = {UserCognitoDTO.FROM_COGNITO_DICT[att["Name"]]: att["Value"] for att in user_data if att["Name"] in UserCognitoDTO.FROM_COGNITO_DICT}
        user_data["created_at"] = data.get("UserCreateDate")
        user_data["updated_at"] = data.get("UserLastModifiedDate")

        return UserCognitoDTO(
            user_id=user_data.get("user_id"),
            email=user_data.get("email"),
            name=user_data.get("name"),
            password=None,
            ra=user_data.get("ra"),
            role=ROLE[user_data.get("role")],
            access_level=ACCESS_LEVEL[user_data.get("access_level")],
            created_at=int(user_data.get("created_at").timestamp()*1000) if user_data.get("created_at") else None,
            updated_at=int(user_data.get("updated_at").timestamp()*1000) if user_data.get("updated_at") else None,
            social_name=user_data.get("social_name"),
            accepted_terms=eval(user_data.get("accepted_terms")),
            accepted_notifications=eval(user_data.get("accepted_notifications")),
            certificate_with_social_name=eval(user_data.get("certificate_with_social_name")),
            phone=user_data.get("phone")
        )

    def to_entity(self) -> User:
        return User(
            user_id=self.user_id,
            email=self.email,
            name=self.name,
            password=self.password,
            ra=self.ra,
            role=self.role,
            access_level=self.access_level,
            created_at=self.created_at,
            updated_at=self.updated_at,
            social_name=self.social_name,
            accepted_terms=self.accepted_terms,
            accepted_notifications=self.accepted_notifications,
            certificate_with_social_name=self.certificate_with_social_name,
            phone=self.phone
        )

    def __eq__(self, other):
        return self.user_id == other.user_id and self.email == other.email and self.name == other.name and self.password == other.password and self.ra == other.ra and self.role == other.role and self.access_level == other.access_level and self.created_at == other.created_at and self.updated_at == other.updated_at and self.social_name == other.social_name and self.accepted_terms == other.accepted_terms and self.accepted_notifications == other.accepted_notifications and self.certificate_with_social_name == other.certificate_with_social_name and self.phone == other.phone

    @staticmethod
    def parse_attribute(name, value) -> dict:
        return {'Name': name, 'Value': str(value)}



