# routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user_schema import UserLogin
from utils.auth import create_access_token, verify_password

router = APIRouter()

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    access_token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "role": db_user.role
    }
