from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.failure import Failure
from models.process import Process
from schemas.failure_schema import FailureCreate, FailureResponse
from database import get_db
from middlewares.auth import verify_jwt

router = APIRouter()

@router.post("/", response_model=FailureResponse, dependencies=[Depends(verify_jwt)])
def create_failure(failure: FailureCreate, request: Request, db: Session = Depends(get_db)):
    process = db.query(Process).filter(Process.id == failure.process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    new_failure = Failure(
        process_id=failure.process_id,
        etapa=failure.etapa,
        descricao=failure.descricao,
        critical=failure.critical,
        usuario_id=failure.usuario_id,
        data=failure.data
    )
    db.add(new_failure)
    db.commit()
    db.refresh(new_failure)
    return new_failure

@router.get("/", response_model=list[FailureResponse], dependencies=[Depends(verify_jwt)])
def list_failures(db: Session = Depends(get_db)):
    return db.query(Failure).all()

@router.get("/by-process/{process_id}", response_model=list[FailureResponse], dependencies=[Depends(verify_jwt)])
def get_failures_by_process(process_id: int, db: Session = Depends(get_db)):
    return db.query(Failure).filter(Failure.process_id == process_id).all()

@router.get("/{failure_id}", response_model=FailureResponse, dependencies=[Depends(verify_jwt)])
def get_failure(failure_id: int, db: Session = Depends(get_db)):
    failure = db.query(Failure).filter(Failure.id == failure_id).first()
    if not failure:
        raise HTTPException(status_code=404, detail="Failure not found")
    return failure
