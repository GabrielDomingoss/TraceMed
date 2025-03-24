from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FailureCreate(BaseModel):
    process_id: int
    etapa: str
    descricao: str
    critical: bool  # <-- AQUI: tem que ser `critical`
    usuario_id: int

class FailureResponse(BaseModel):
    id: int
    process_id: int
    etapa: str
    descricao: str
    critical: bool
    data: datetime
    usuario_id: int

    class Config:
        from_attributes = True