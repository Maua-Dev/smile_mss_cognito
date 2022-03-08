from typing import Optional, List

from pydantic.main import BaseModel

from pydantic import validator

from src.domain.errors.errors import EntityError


class User(BaseModel):
    name: str
    cpfRne: int
    role: str

    @validator('name')
    def name_is_not_empty(cls,v: str)-> str:
        if len(v) == 0:
            raise EntityError('Name')
        return v.title()

    @validator('cpfRne')
    def cpfRne_is_not_invalid(cls, v: int) -> int:
        if len(str(v)) != 11:
            raise EntityError('cpfRne')
        return v

    @validator('role')
    def role_is_not_empty(cls, v: List[int]) -> List[int]:
        if len(v) == 0:
            raise EntityError('role')
        return v