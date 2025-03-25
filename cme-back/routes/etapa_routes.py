# routes/etapa_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models.process import Process
from models.failure import Failure
from schemas.process_schema import EtapaUpdate
from middlewares.auth import verificar_jwt

router = APIRouter()

@router.put("/etapa/{process_id}/{etapa}", response_model=dict, dependencies=[Depends(verificar_jwt)])
def update_stage(process_id: int, etapa: str, dados: EtapaUpdate, request: Request, db: Session = Depends(get_db)):
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    falha_critica = db.query(Failure).filter(
        Failure.process_id == process_id,
        Failure.critical == True
    ).first()

    if falha_critica:
        raise HTTPException(status_code=400, detail="Cannot update stages after a critical failure")

    if etapa == "recebimento":
        process.data_recebimento = dados.data
        process.observacao_recebimento = dados.observacao
        process.usuario_recebimento_id = dados.usuario_id
    elif etapa == "lavagem":
        process.data_lavagem = dados.data
        process.observacao_lavagem = dados.observacao
        process.usuario_lavagem_id = dados.usuario_id
    elif etapa == "esterilizacao":
        process.data_esterilizacao = dados.data
        process.observacao_esterilizacao = dados.observacao
        process.usuario_esterilizacao_id = dados.usuario_id
    elif etapa == "distribuicao":
        process.data_distribuicao = dados.data
        process.observacao_distribuicao = dados.observacao
        process.usuario_distribuicao_id = dados.usuario_id
    else:
        raise HTTPException(status_code=400, detail="Invalid stage")

    db.commit()
    db.refresh(process)
    return {"message": f"Stage '{etapa}' updated successfully"}
