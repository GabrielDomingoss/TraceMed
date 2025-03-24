from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    
    data_recebimento = Column(DateTime, nullable=True)
    observacao_recebimento = Column(String(255), nullable=True)
    usuario_recebimento_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    data_lavagem = Column(DateTime, nullable=True)
    observacao_lavagem = Column(String(255), nullable=True)
    usuario_lavagem_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    data_esterilizacao = Column(DateTime, nullable=True)
    observacao_esterilizacao = Column(String(255), nullable=True)
    usuario_esterilizacao_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    data_distribuicao = Column(DateTime, nullable=True)
    observacao_distribuicao = Column(String(255), nullable=True)
    usuario_distribuicao_id = Column(Integer, ForeignKey("users.id"), nullable=True)


    criado_em = Column(DateTime, default=datetime.utcnow)

    material = relationship("Material", back_populates="processes")
    failures = relationship("Failure", back_populates="process", cascade="all, delete")

    usuario_recebimento = relationship("User", foreign_keys=[usuario_recebimento_id])
    usuario_lavagem = relationship("User", foreign_keys=[usuario_lavagem_id])
    usuario_esterilizacao = relationship("User", foreign_keys=[usuario_esterilizacao_id])
    usuario_distribuicao = relationship("User", foreign_keys=[usuario_distribuicao_id])