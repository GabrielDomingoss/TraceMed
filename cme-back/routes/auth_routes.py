# routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user_schema import UserLogin, TokenResponse
from utils.jwt_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=token)
