from enum import Enum


class ROLE(Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    PROFESSOR = "PROFESSOR"
    INTERNATIONAL_STUDENT = "INTERNATIONAL_STUDENT"
    EXTERNAL = "EXTERNAL"

    def __str__(self):
        return self.value


class ACCESS_LEVEL(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    SPEAKER = "SPEAKER"

    def __str__(self):
        return self.value
