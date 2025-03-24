# auth/handler.py
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "seu_segredo_super_secreto"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60

def criar_token(dados: dict):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
