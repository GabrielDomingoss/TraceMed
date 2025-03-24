from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.material import Material
from schemas.material_schema import MaterialCreate, MaterialResponse
from auth.dependencies import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MaterialResponse)
def create_material(material: MaterialCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    novo_material = Material(
        nome=material.nome,
        tipo=material.tipo,
        data_validade=material.data_validade
    )
    db.add(novo_material)
    db.commit()
    db.refresh(novo_material)
    return novo_material

@router.get("/", response_model=list[MaterialResponse])
def list_materials(db: Session = Depends(get_db)):
    return db.query(Material).all()