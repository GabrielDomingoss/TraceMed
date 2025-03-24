# auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.handler import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
