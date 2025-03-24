from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from database import get_db
from utils.auth import get_password_hash
from middlewares.auth import verificar_jwt

router = APIRouter()

# Apenas admin pode acessar
def verificar_admin(request: Request):
    if request.state.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado: apenas administradores")

@router.get("/", response_model=list[UserResponse], dependencies=[Depends(verificar_jwt)])
def listar_usuarios(request: Request, db: Session = Depends(get_db)):
    verificar_admin(request)
    usuarios = db.query(User).all()
    return usuarios

@router.post("/", response_model=UserResponse, dependencies=[Depends(verificar_jwt)])
def criar_usuario(usuario: UserCreate, request: Request, db: Session = Depends(get_db)):
    verificar_admin(request)

    usuario_existente = db.query(User).filter(User.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    senha_hash = get_password_hash(usuario.password)
    novo_usuario = User(
        name=usuario.name,
        email=usuario.email,
        password=senha_hash,
        role=usuario.role
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(verificar_jwt)])
def obter_usuario(user_id: int, request: Request, db: Session = Depends(get_db)):
    verificar_admin(request)
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(verificar_jwt)])
def atualizar_usuario(user_id: int, dados: UserUpdate, request: Request, db: Session = Depends(get_db)):
    verificar_admin(request)
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if dados.name:
        usuario.name = dados.name
    if dados.email:
        usuario.email = dados.email
    if dados.password:
        usuario.password = get_password_hash(dados.password)
    if dados.role:
        usuario.role = dados.role

    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{user_id}", dependencies=[Depends(verificar_jwt)])
def deletar_usuario(user_id: int, request: Request, db: Session = Depends(get_db)):
    verificar_admin(request)
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()
    return {"mensagem": "Usuário deletado com sucesso"}
