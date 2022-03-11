from enum import Enum


class ROLE(Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    PROFESSOR = "PROFESSOR"

    def __str__(self):
        return self.value


class ACCESS_LEVEL(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

    def __str__(self):
        return self.value