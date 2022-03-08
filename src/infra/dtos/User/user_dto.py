from src.infra.dtos.db_base import Base


class UserDTO(Base):
    id: int
    proprieties: dict[str, str]

