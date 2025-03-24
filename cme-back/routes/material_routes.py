from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models.material import Material
from schemas.material_schema import MaterialCreate, MaterialResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MaterialResponse)
def create_material(material: MaterialCreate, db: Session = Depends(get_db), request: Request = None):
    role = request.state.role
    
    if role not in ["tecnico", "admin"]:
        raise HTTPException(status_code=403, detail="Permissão negada")
    
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
def list_materials(db: Session = Depends(get_db), request: Request = None):
    return db.query(Material).all()