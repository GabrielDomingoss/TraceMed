from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Failure(Base):
    __tablename__ = "failures"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)
    etapa = Column(String(50), nullable=False)
    descricao = Column(String(255), nullable=False)
    critical = Column(Boolean, default=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    data = Column(DateTime, default=datetime.utcnow)  # <-- Aqui

    process = relationship("Process", back_populates="failures")
    usuario = relationship("User")
