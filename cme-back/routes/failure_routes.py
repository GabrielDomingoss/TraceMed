from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
from models.failure import Failure
from models.process import Process
from schemas.failure_schema import FailureCreate, FailureResponse
from datetime import datetime

router = APIRouter()

# Dependência para obter DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - Cadastrar nova falha
@router.post("/", response_model=FailureResponse)
def registrar_falha(falha: FailureCreate, db: Session = Depends(get_db)):
    print(f"Recebido: {falha.dict()}")  # <- Isso ajuda bastante
    nova_falha = Failure(
        process_id=falha.process_id,
        etapa=falha.etapa,
        descricao=falha.descricao,
        critical=falha.critical,
        usuario_id=falha.usuario_id
    )
    db.add(nova_falha)
    db.commit()
    db.refresh(nova_falha)
    return nova_falha

# GET - Listar failures por processo
@router.get("/processo/{process_id}", response_model=list[FailureResponse])
def listar_falhas_por_processo(process_id: int, db: Session = Depends(get_db)):
    failures = db.query(Failure).filter(Failure.process_id == process_id).all()
    if not failures:
        raise HTTPException(status_code=404, detail="Nenhuma falha encontrada para este processo.")
    return failures

@router.get("/", response_model=List[FailureResponse])
def listar_falhas(
    process_id: Optional[int] = None,
    etapa: Optional[str] = None,
    critical: Optional[bool] = None,
    data_inicio: Optional[datetime] = Query(None, alias="data_inicio"),
    data_fim: Optional[datetime] = Query(None, alias="data_fim"),
    db: Session = Depends(get_db)
):
    query = db.query(Failure)

    if process_id:
        query = query.filter(Failure.process_id == process_id)
    if etapa:
        query = query.filter(Failure.etapa == etapa)
    if critical is not None:
        query = query.filter(Failure.critical == critical)
    if data_inicio:
        query = query.filter(Failure.data >= data_inicio)
    if data_fim:
        query = query.filter(Failure.data <= data_fim)

    return query.order_by(Failure.data.desc()).all()

@router.get("/process/{process_id}", response_model=list[FailureResponse])
def listar_falhas_por_processo(process_id: int, db: Session = Depends(get_db)):
    failures = db.query(Failure).filter(Failure.process_id == process_id).order_by(Failure.data.desc()).all()
    if not failures:
        raise HTTPException(status_code=404, detail="Nenhuma falha encontrada para este processo.")
    return failures
