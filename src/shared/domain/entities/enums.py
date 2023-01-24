from enum import Enum


class ROLE(Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    PROFESSOR = "PROFESSOR"
    SPEAKER = "SPEAKER"

    def __str__(self):
        return self.value


class ACCESS_LEVEL(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    SPEAKER = "SPEAKER"

    def __str__(self):
        return self.value