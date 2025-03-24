from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from typing import List, Optional
from models.material import Material
from models.process import Process
from models.failure import Failure
from schemas.process_schema import ProcessCreate, ProcessResponse, RastreabilidadeResponse, DetalhesProcessoResponse, EtapaInfo, MaterialInfo
from schemas.user_schema import UserSimple, UserResponse
from schemas.failure_schema import FailureResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProcessResponse)
def registrar_etapa(process: ProcessCreate, db: Session = Depends(get_db), request: Request = None):
    role = request.state.role
    if role not in ["tecnico", "admin"]:
        raise HTTPException(status_code=403, detail="Permissão negada")
    
    # 1. Buscar material pelo serial
    material = db.query(Material).filter(Material.serial == process.serial_material).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")

    # 2. Criar novo processo
    novo_processo = Process(material_id=material.id)

    # 3. Preencher os dados da etapa com base no nome da etapa enviada
    etapa = process.etapa
    etapa_data = getattr(process, etapa, None)

    if not etapa_data:
        raise HTTPException(status_code=400, detail=f"Dados da etapa '{etapa}' não foram fornecidos.")

    if etapa == "recebimento":
        novo_processo.data_recebimento = etapa_data.data
        novo_processo.observacao_recebimento = etapa_data.observacao
        novo_processo.usuario_recebimento_id = etapa_data.usuario_id
    elif etapa == "lavagem":
        novo_processo.data_lavagem = etapa_data.data
        novo_processo.observacao_lavagem = etapa_data.observacao
        novo_processo.usuario_lavagem_id = etapa_data.usuario_id
    elif etapa == "esterilizacao":
        novo_processo.data_esterilizacao = etapa_data.data
        novo_processo.observacao_esterilizacao = etapa_data.observacao
        novo_processo.usuario_esterilizacao_id = etapa_data.usuario_id
    elif etapa == "distribuicao":
        novo_processo.data_distribuicao = etapa_data.data
        novo_processo.observacao_distribuicao = etapa_data.observacao
        novo_processo.usuario_distribuicao_id = etapa_data.usuario_id
    else:
        raise HTTPException(status_code=400, detail="Etapa inválida.")

    db.add(novo_processo)
    db.commit()
    db.refresh(novo_processo)
    return novo_processo

@router.get("/", response_model=List[DetalhesProcessoResponse])
def listar_processos(
    role: Optional[str] = Query(None, description="Tipo de usuário: tecnico, enfermeiro ou admin"),
    etapa_atual: Optional[str] = Query(None, description="Etapa atual: recebimento, lavagem, esterilizacao, distribuicao"),
    interrompido: Optional[bool] = Query(None, description="Se o processo foi interrompido por falha crítica"),
    com_falha: Optional[bool] = Query(None, description="Se o processo possui pelo menos uma falha"),
    db: Session = Depends(get_db),
    request: Request = None
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
                "usuario": UserResponse.model_validate(p.usuario_recebimento) if p.usuario_recebimento else None
            } if p.data_recebimento else None,
            lavagem={
                "data": p.data_lavagem,
                "observacao": p.observacao_lavagem,
                "usuario": UserResponse.model_validate(p.usuario_lavagem) if p.usuario_lavagem else None
            } if p.data_lavagem else None,
            esterilizacao={
                "data": p.data_esterilizacao,
                "observacao": p.observacao_esterilizacao,
                "usuario": UserResponse.model_validate(p.usuario_esterilizacao) if p.usuario_esterilizacao else None
            } if p.data_esterilizacao else None,
            distribuicao={
                "data": p.data_distribuicao,
                "observacao": p.observacao_distribuicao,
                "usuario": UserResponse.model_validate(p.usuario_distribuicao) if p.usuario_distribuicao else None
            } if p.data_distribuicao else None,
            falhas=p.failures,
            interrompido_por_falha_critica=any(f.critical for f in p.failures)
        )
        resultados.append(resultado)

    return resultados

@router.get("/by-serial/{serial}", response_model=list[ProcessResponse])
def listar_etapas_por_serial(serial: str, db: Session = Depends(get_db)):
    etapas = db.query(Process).filter(Process.material_id == serial).order_by(Process.criado_em.asc()).all()
    if not etapas:
        raise HTTPException(status_code=404, detail="Nenhum processo encontrado para este serial.")
    return etapas

@router.get("/{process_id}/rastreabilidade", response_model=RastreabilidadeResponse)
def rastrear_processo(process_id: int, db: Session = Depends(get_db)):
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrado")

    def etapa_info(data, obs, usuario):
        if not data and not obs and not usuario:
            return None
        return {
            "data": data,
            "observacao": obs,
            "usuario": usuario
        }

    return {
        "id": process.id,
        "material": process.material,
        "recebimento": etapa_info(
            process.data_recebimento,
            process.observacao_recebimento,
            process.usuario_recebimento
        ),
        "lavagem": etapa_info(
            process.data_lavagem,
            process.observacao_lavagem,
            process.usuario_lavagem
        ),
        "esterilizacao": etapa_info(
            process.data_esterilizacao,
            process.observacao_esterilizacao,
            process.usuario_esterilizacao
        ),
        "distribuicao": etapa_info(
            process.data_distribuicao,
            process.observacao_distribuicao,
            process.usuario_distribuicao
        ),
        "failures": process.failures
    }

@router.get("/detalhes/{process_id}", response_model=DetalhesProcessoResponse)
def detalhes_processo(process_id: int, db: Session = Depends(get_db)):
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrado")

    def build_etapa(data, observacao, usuario):
        if not data:
            return None
        return EtapaInfo (
            data=data,
            observacao=observacao,
            usuario=UserSimple(
                id=usuario.id,
                name=usuario.name,
                email=usuario.email,
                role=usuario.role
            ) if usuario else None
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

    processo_detalhado = DetalhesProcessoResponse(
        id=process.id,
        material=MaterialInfo(
            id=process.material.id,
            nome=process.material.nome,
            tipo=process.material.tipo,
            data_validade=process.material.data_validade,
            serial=process.material.serial,
        ),
        recebimento=build_etapa(process.data_recebimento, process.observacao_recebimento, process.usuario_recebimento),
        lavagem=build_etapa(process.data_lavagem, process.observacao_lavagem, process.usuario_lavagem),
        esterilizacao=build_etapa(process.data_esterilizacao, process.observacao_esterilizacao, process.usuario_esterilizacao),
        distribuicao=build_etapa(process.data_distribuicao, process.observacao_distribuicao, process.usuario_distribuicao),
        falhas=falhas_response,
        interrompido_por_falha_critica=any(f.critical for f in falhas)
    )

    return processo_detalhado