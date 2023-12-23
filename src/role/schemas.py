from typing import Optional
from pydantic import BaseModel, Field


class RoleGet(BaseModel):
    id: int
    name: str
    permissions: Optional[str]


class RoleCreate(BaseModel):
    id: int
    name: str = Field(..., title="Должность")


# формальность
class RoleUpdate(BaseModel):
    name: str = Field(..., title="Должность")


