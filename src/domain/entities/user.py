from datetime import datetime
from typing import Optional, List
from pydantic.main import BaseModel
from pydantic import validator
import re

from src.domain.entities.enums import ROLE, ACCESS_LEVEL
from src.domain.errors.errors import EntityError


class User(BaseModel):
    id: Optional[str]
    name: str
    cpfRne: str
    password: Optional[str]
    ra: Optional[int]
    email: Optional[str]
    role: ROLE
    accessLevel: ACCESS_LEVEL
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    socialName: Optional[str]
    acceptedTerms: Optional[bool]
    acceptedNotifications: Optional[bool]
    certificateWithSocialName: Optional[bool]


    @staticmethod
    def validateCpf(cpf: str) -> bool:
        # Verifica a formatação do CPF
        if not re.match(r'\d{11}', cpf):
            return False

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    @validator('name')
    def name_is_not_empty(cls,v: str)-> str:
        if len(v) == 0:
            raise EntityError('Name')
        return v.title() #todo é isso mesmo?

    @validator('cpfRne')
    def cpfRne_is_not_invalid(cls, v: int) -> int:
        if not User.validateCpf(v):
            raise EntityError('cpfRne')
        return v

    @validator('ra')
    def ra_is_not_invalid(cls, v: int) -> int:
        if v != None and len(str(v)) != 8:
            raise EntityError('ra')
        return v

    @validator('createdAt')
    def createdAt_is_not_empty(cls, v: datetime) -> datetime:
        return v

    @validator('updatedAt')
    def updatedAt_is_not_empty(cls, v: datetime) -> datetime:
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

    @validator('socialName')
    def socialName_is_not_empty(cls, v: str) -> str:
        if v and len(v) == 0:
            raise EntityError('socialName')
        return v

    @validator('acceptedTerms')
    def acceptedTerms_is_not_bool(cls, v: bool) -> bool:
        if not v and v is not None:
            raise EntityError('acceptedTerms')
        return v

    @validator('acceptedNotifications')
    def acceptedNotifications_is_not_bool(cls, v: bool) -> bool:
        if v and not isinstance(v, bool):
            raise EntityError('acceptedNotifications')
        return v

    @validator('certificateWithSocialName')
    def certificateWithSocialName_is_not_bool(cls, v: bool) -> bool:
        if v and not isinstance(v, bool):
            raise EntityError('certificateWithSocialName')
        return v




