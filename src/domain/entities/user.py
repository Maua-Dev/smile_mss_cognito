from datetime import datetime
from typing import Optional, List
from pydantic.main import BaseModel
from pydantic import validator
import re

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.errors.errors import EntityError


class User(BaseModel):
    name: str
    cpfRne: int
    password: Optional[str]
    ra: Optional[int]
    email: Optional[str]
    role: ROLE
    accessLevel: ACCESS_LEVEL
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


    @validator('name')
    def name_is_not_empty(cls,v: str)-> str:
        if len(v) == 0:
            raise EntityError('Name')
        return v.title() #todo é isso mesmo?

    @validator('cpfRne')
    def cpfRne_is_not_invalid(cls, v: int) -> int:
        if len(str(v)) != 11:
            raise EntityError('cpfRne')
        return v

    @validator('ra')
    def ra_is_not_invalid(cls, v: int) -> int:
        if len(str(v)) != 8:
            raise EntityError('ra')
        return v

    @validator('createdAt')
    def createdAt_is_not_empty(cls, v: datetime) -> datetime:
        if v is None:
            raise EntityError('createdAt')
        return v

    @validator('updatedAt')
    def updatedAt_is_not_empty(cls, v: datetime) -> datetime:
        if v is None:
            raise EntityError('updatedAt')
        return v

    @validator('role')
    def role_is_not_empty(cls, v: List[int]) -> List[int]:
        if v is None:
            raise EntityError('role')
        return v

    @validator('accessLevel')
    def accessLevel_is_not_empty(cls, v: List[int]) -> List[int]:
        if v is None:
            raise EntityError('accessLevel')
        return v

    @validator('email')
    def email_is_valid(cls, v: str) -> str:
        if not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', v):
            raise EntityError('email')
        return v



