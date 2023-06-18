from pydantic import BaseModel


class StatusGet(BaseModel):
    id: int
    name: str


class StatusCreate(BaseModel):
    id: int
    name: str


class StatusUpdate(BaseModel):
    id: int
    name: str

