from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(100), nullable=False)
    data_validade = Column(Date, nullable=False)
    serial = Column(String(100), unique=True, index=True)
    processes = relationship("Process", back_populates="material")

    def __init__(self, nome, tipo, data_validade):
        self.nome = nome
        self.tipo = tipo
        self.data_validade = data_validade
        self.serial = f"{nome[:3].upper()}-{uuid.uuid4().hex[:6]}"