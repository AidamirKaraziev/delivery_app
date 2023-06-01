from datetime import datetime
from sqlite3 import Date

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str


class OperationGet(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: Date
    type: str
