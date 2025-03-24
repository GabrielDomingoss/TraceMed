# routes/etapa_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models.process import Process
from models.failure import Failure
from schemas.process_schema import EtapaUpdate

router = APIRouter()

@router.put("/{process_id}/{etapa}", response_model=dict)
def atualizar_etapa(process_id: int, etapa: str, dados: EtapaUpdate, db: Session = Depends(get_db), request: Request = None):
    role = request.state.role
    if role not in ["tecnico", "admin"]:
        raise HTTPException(status_code=403, detail="Permissão negada")
    
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrado")

    falha_critica = db.query(Failure).filter(
        Failure.process_id == process_id,
        Failure.critical == True
    ).first()

    if falha_critica:
        raise HTTPException(status_code=400, detail="Não é possível atualizar etapas após uma falha crítica.")

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
        raise HTTPException(status_code=400, detail="Etapa inválida.")

    db.commit()
    db.refresh(process)
    return {"mensagem": f"Etapa '{etapa}' atualizada com sucesso"}
