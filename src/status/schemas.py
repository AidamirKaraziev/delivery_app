from pydantic import BaseModel


class StatusGet(BaseModel):
    id: int
    name: str
