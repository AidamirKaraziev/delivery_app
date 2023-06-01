from typing import Optional
from fastapi import Request

# from app.core.config import Settings, settings


from operations.schemas import OperationGet


#               config: Settings = settings, , request: Optional[Request]
def get_operation(operation: OperationGet) -> Optional[OperationGet]:

    return OperationGet(
        id=operation.id,
        quantity=operation.quantity,
        figi=operation.figi,
        instrument_type=operation.instrument_type,
        date=operation.date,
        type=operation.type
    )

