from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from database import get_db
from utils.auth import get_password_hash
from middlewares.auth import verify_jwt

router = APIRouter()

# Admin role check
def verify_admin(request: Request):
    if request.state.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied: admin only")

@router.get("/", response_model=list[UserResponse], dependencies=[Depends(verify_jwt)])
def list_users(request: Request, db: Session = Depends(get_db)):
    verify_admin(request)
    users = db.query(User).all()
    return users

@router.post("/", response_model=UserResponse, dependencies=[Depends(verify_jwt)])
def create_user(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    verify_admin(request)

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password = user.password or "teste123"
    hashed_password = get_password_hash(password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_jwt)])
def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    verify_admin(request)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_jwt)])
def update_user(user_id: int, data: UserUpdate, request: Request, db: Session = Depends(get_db)):
    verify_admin(request)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email
    if data.password:
        user.password = get_password_hash(data.password)
    if data.role:
        user.role = data.role

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", dependencies=[Depends(verify_jwt)])
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    verify_admin(request)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
