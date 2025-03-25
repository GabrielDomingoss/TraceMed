# routes/process_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from typing import List, Optional
from models.material import Material
from models.process import Process
from models.failure import Failure
from schemas.process_schema import (
    ProcessCreate,
    ProcessResponse,
    RastreabilidadeResponse,
    DetalhesProcessoResponse,
    EtapaInfo,
    MaterialInfo
)
from schemas.user_schema import UserSimple
from schemas.failure_schema import FailureResponse
from middlewares.auth import verify_jwt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProcessResponse, dependencies=[Depends(verify_jwt)])
def register_stage(process: ProcessCreate, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.serial == process.serial_material).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    new_process = Process(material_id=material.id)
    etapa = process.etapa
    etapa_data = getattr(process, etapa, None)

    if not etapa_data:
        raise HTTPException(status_code=400, detail=f"Step data '{etapa}' not provided.")

    if etapa == "recebimento":
        new_process.data_recebimento = etapa_data.data
        new_process.observacao_recebimento = etapa_data.observacao
        new_process.usuario_recebimento_id = etapa_data.usuario_id
    elif etapa == "lavagem":
        new_process.data_lavagem = etapa_data.data
        new_process.observacao_lavagem = etapa_data.observacao
        new_process.usuario_lavagem_id = etapa_data.usuario_id
    elif etapa == "esterilizacao":
        new_process.data_esterilizacao = etapa_data.data
        new_process.observacao_esterilizacao = etapa_data.observacao
        new_process.usuario_esterilizacao_id = etapa_data.usuario_id
    elif etapa == "distribuicao":
        new_process.data_distribuicao = etapa_data.data
        new_process.observacao_distribuicao = etapa_data.observacao
        new_process.usuario_distribuicao_id = etapa_data.usuario_id
    else:
        raise HTTPException(status_code=400, detail="Invalid stage.")

    db.add(new_process)
    db.commit()
    db.refresh(new_process)
    return new_process

@router.get("/", response_model=List[DetalhesProcessoResponse], dependencies=[Depends(verify_jwt)])
def list_processes(
    role: Optional[str] = Query(None),
    etapa_atual: Optional[str] = Query(None),
    interrompido: Optional[bool] = Query(None),
    com_falha: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    processos = db.query(Process).options(
        joinedload(Process.material),
        joinedload(Process.usuario_recebimento),
        joinedload(Process.usuario_lavagem),
        joinedload(Process.usuario_esterilizacao),
        joinedload(Process.usuario_distribuicao),
        joinedload(Process.failures)
    ).all()

    resultados = []
    for p in processos:
        resultado = DetalhesProcessoResponse(
            id=p.id,
            material=p.material,
            recebimento={
                "data": p.data_recebimento,
                "observacao": p.observacao_recebimento,
                "usuario": UserSimple.model_validate(p.usuario_recebimento) if p.usuario_recebimento else None
            } if p.data_recebimento else None,
            lavagem={
                "data": p.data_lavagem,
                "observacao": p.observacao_lavagem,
                "usuario": UserSimple.model_validate(p.usuario_lavagem) if p.usuario_lavagem else None
            } if p.data_lavagem else None,
            esterilizacao={
                "data": p.data_esterilizacao,
                "observacao": p.observacao_esterilizacao,
                "usuario": UserSimple.model_validate(p.usuario_esterilizacao) if p.usuario_esterilizacao else None
            } if p.data_esterilizacao else None,
            distribuicao={
                "data": p.data_distribuicao,
                "observacao": p.observacao_distribuicao,
                "usuario": UserSimple.model_validate(p.usuario_distribuicao) if p.usuario_distribuicao else None
            } if p.data_distribuicao else None,
            falhas=p.failures,
            interrompido_por_falha_critica=any(f.critical for f in p.failures)
        )
        resultados.append(resultado)

    return resultados

@router.get("/by-serial/{serial}", response_model=List[ProcessResponse], dependencies=[Depends(verify_jwt)])
def list_by_serial(serial: str, db: Session = Depends(get_db)):
    etapas = db.query(Process).filter(Process.material_id == serial).order_by(Process.criado_em.asc()).all()
    if not etapas:
        raise HTTPException(status_code=404, detail="No process found for this serial.")
    return etapas

@router.get("/{process_id}/rastreabilidade", response_model=RastreabilidadeResponse, dependencies=[Depends(verify_jwt)])
def traceability(process_id: int, db: Session = Depends(get_db)):
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    def etapa_info(data, obs, usuario):
        if not data and not obs and not usuario:
            return None
        return {
            "data": data,
            "observacao": obs,
            "usuario": UserSimple.model_validate(usuario) if usuario else None
        }

    return {
        "id": process.id,
        "material": process.material,
        "recebimento": etapa_info(process.data_recebimento, process.observacao_recebimento, process.usuario_recebimento),
        "lavagem": etapa_info(process.data_lavagem, process.observacao_lavagem, process.usuario_lavagem),
        "esterilizacao": etapa_info(process.data_esterilizacao, process.observacao_esterilizacao, process.usuario_esterilizacao),
        "distribuicao": etapa_info(process.data_distribuicao, process.observacao_distribuicao, process.usuario_distribuicao),
        "failures": process.failures
    }

@router.get("/detalhes/{process_id}", response_model=DetalhesProcessoResponse, dependencies=[Depends(verify_jwt)])
def process_details(process_id: int, db: Session = Depends(get_db)):
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    def build_etapa(data, observacao, usuario):
        if not data:
            return None
        return EtapaInfo(
            data=data,
            observacao=observacao,
            usuario=UserSimple.model_validate(usuario) if usuario else None
        )

    falhas = db.query(Failure).filter(Failure.process_id == process.id).all()
    falhas_response = [
        FailureResponse(
            id=f.id,
            process_id=f.process_id,
            etapa=f.etapa,
            descricao=f.descricao,
            critical=f.critical,
            data=f.data,
            usuario_id=f.usuario_id
        ) for f in falhas
    ]

    return DetalhesProcessoResponse(
        id=process.id,
        material=MaterialInfo(
            id=process.material.id,
            nome=process.material.nome,
            tipo=process.material.tipo,
            data_validade=process.material.data_validade,
            serial=process.material.serial
        ),
        recebimento=build_etapa(process.data_recebimento, process.observacao_recebimento, process.usuario_recebimento),
        lavagem=build_etapa(process.data_lavagem, process.observacao_lavagem, process.usuario_lavagem),
        esterilizacao=build_etapa(process.data_esterilizacao, process.observacao_esterilizacao, process.usuario_esterilizacao),
        distribuicao=build_etapa(process.data_distribuicao, process.observacao_distribuicao, process.usuario_distribuicao),
        falhas=falhas_response,
        interrompido_por_falha_critica=any(f.critical for f in falhas)
    )
