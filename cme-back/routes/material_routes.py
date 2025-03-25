# routes/material_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.material import Material
from schemas.material_schema import MaterialCreate, MaterialResponse, MaterialUpdate
from database import get_db
from middlewares.auth import verify_jwt

router = APIRouter()

@router.get("/", response_model=list[MaterialResponse], dependencies=[Depends(verify_jwt)])
def list_materials(db: Session = Depends(get_db)):
    materials = db.query(Material).all()
    return materials

@router.post("/", response_model=MaterialResponse, dependencies=[Depends(verify_jwt)])
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    existing = db.query(Material).filter(Material.serial == material.serial).first()
    if existing:
        raise HTTPException(status_code=400, detail="Material already registered")

    new_material = Material(
        nome=material.nome,
        tipo=material.tipo,
        data_validade=material.data_validade,
        serial=material.serial
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

@router.get("/{material_id}", response_model=MaterialResponse, dependencies=[Depends(verify_jwt)])
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.put("/{material_id}", response_model=MaterialResponse, dependencies=[Depends(verify_jwt)])
def update_material(material_id: int, data: MaterialUpdate, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    if data.nome is not None:
        material.nome = data.nome
    if data.tipo is not None:
        material.tipo = data.tipo
    if data.data_validade is not None:
        material.data_validade = data.data_validade
    if data.serial is not None:
        material.serial = data.serial

    db.commit()
    db.refresh(material)
    return material

@router.delete("/{material_id}", dependencies=[Depends(verify_jwt)])
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    db.delete(material)
    db.commit()
    return {"message": "Material deleted successfully"}
