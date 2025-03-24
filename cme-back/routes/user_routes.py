# routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserResponse, UserLogin, TokenResponse
from models.user import User
from database import get_db
from auth.handler import criar_token
from passlib.context import CryptContext
from auth.dependencies import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_pw = pwd_context.hash(user.password)
    novo_user = User(name=user.name, email=user.email, password=hashed_pw, role=user.role)
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db or not pwd_context.verify(user.password, user_db.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    token = criar_token({"sub": user_db.email, "id": user_db.id, "role": user_db.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    return user
