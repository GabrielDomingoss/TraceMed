from pydantic import BaseModel
from datetime import date
from typing import Optional

class MaterialBase(BaseModel):
    nome: str
    tipo: str
    data_validade: date

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    nome: Optional[str]
    tipo: Optional[str]
    data_validade: Optional[str] 

class MaterialResponse(MaterialBase):
    id: int
    serial: str

    class Config:
        from_attributes = True