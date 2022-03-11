from pydantic.main import BaseModel
from datetime import datetime
from typing import Optional

from src.domain.entities.enums import ACCESS_LEVEL, ROLE


class DbBaseModel():
    name: str
    cpfRne: int
    password: Optional[str]
    ra: Optional[int]
    email: Optional[str]
    role: ROLE
    accessLevel: ACCESS_LEVEL
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

    def __init__(self, data: dict):
        self.name = data.get('name')
        self.cpfRne = data.get('cpfRne')
        self.password = data.get('password')
        self.ra = data.get('ra')
        self.email = data.get('email')
        self.role = data.get('role')
        self.accessLevel = data.get('accessLevel')
        # self.createdAt = data.get('createdAt')
        # self.updatedAt = data.get('updatedAt')

    def to_dict(self):
        return self.__dict__



