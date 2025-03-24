from pydantic import BaseModel
from datetime import date

class MaterialBase(BaseModel):
    nome: str
    tipo: str
    data_validade: date

class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    id: int
    serial: str

    class Config:
        from_attributes = True