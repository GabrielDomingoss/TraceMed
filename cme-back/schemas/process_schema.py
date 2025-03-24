from pydantic import BaseModel
from typing import Optional, List
from schemas.failure_schema import FailureResponse
from datetime import datetime
from schemas.user_schema import UserSimple
from schemas.material_schema import MaterialResponse
from schemas.user_schema import UserResponse

class EtapaInfo(BaseModel):
    data: Optional[datetime]
    observacao: Optional[str]
    usuario: Optional[UserResponse]

    class Config:
        from_attributes = True

class FalhaInfo(BaseModel):
    etapa: str
    descricao: str
    critical: bool
    data: datetime

    class Config:
        from_attributes = True

class MaterialInfo(BaseModel):
    id: int
    nome: str
    serial: str

    class Config:
        from_attributes = True

class RastreabilidadeResponse(BaseModel):
    id: int
    material: MaterialResponse
    recebimento: Optional[EtapaInfo]
    lavagem: Optional[EtapaInfo]
    esterilizacao: Optional[EtapaInfo]
    distribuicao: Optional[EtapaInfo]
    failures: List[FailureResponse]

    class Config:
        from_attributes = True

class EtapaBase(BaseModel):
    data: Optional[datetime] = None
    observacao: Optional[str] = None
    usuario_id: Optional[int] = None

class EtapaUpdate(BaseModel):
    etapa: str
    data: datetime
    observacao: Optional[str] = None
    usuario_id: int

class ProcessBase(BaseModel):
    pass

class ProcessCreate(ProcessBase):
    serial_material: str
    etapa: Optional[str] = None
    recebimento: Optional[EtapaBase] = None
    lavagem: Optional[EtapaBase] = None
    esterilizacao: Optional[EtapaBase] = None
    distribuicao: Optional[EtapaBase] = None


class ProcessResponse(ProcessBase):
    id: int
    criado_em: datetime  # <-- ajustar aqui
    recebimento: Optional[EtapaBase] = None
    lavagem: Optional[EtapaBase] = None
    esterilizacao: Optional[EtapaBase] = None
    distribuicao: Optional[EtapaBase] = None
    failures: List[FailureResponse] = []
    
    class Config:
        from_attributes = True

class DetalhesProcessoResponse(BaseModel):
    id: int
    material: MaterialResponse
    recebimento: Optional[EtapaInfo]
    lavagem: Optional[EtapaInfo]
    esterilizacao: Optional[EtapaInfo]
    distribuicao: Optional[EtapaInfo]
    falhas: List[FailureResponse]
    interrompido_por_falha_critica: bool

    class Config:
        from_attributes = True