from typing import Optional

from pydantic import BaseModel

from src.domain.entities.enums import ROLE, ACCESS_LEVEL


class GetUserModel(BaseModel):
    name: str
    cpfRne: int
    email: Optional[str]
    ra: Optional[int]
    role: ROLE
    accessLevel: ACCESS_LEVEL
    socialName: Optional[str]




