from pydantic import BaseModel


class GetUserModel(BaseModel):
    name: str
    cpfRne: int

