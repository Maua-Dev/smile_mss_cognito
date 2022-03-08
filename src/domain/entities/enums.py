from enum import Enum


class ROLE(Enum):
    ADMIN = "admin"
    STUDENT = "user"
    PROFESSOR = "professor"


class ACCESS_LEVEL(Enum):
    ADMIN = "admin"
    USER = "user"