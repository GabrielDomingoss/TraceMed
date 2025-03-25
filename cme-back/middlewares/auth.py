from fastapi import Request, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from utils.auth import decode_access_token
from jose import JWTError 

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ignora rotas públicas (ex: /login)
        if request.url.path.startswith("/api/auth"):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token JWT não fornecido")

        try:
            payload = decode_access_token(token.split(" ")[1])
            request.state.user_id = payload.get("sub")
            request.state.role = payload.get("role")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token JWT inválido")

        return await call_next(request)

# Funções auxiliares de permissão

def verify_jwt(request: Request):
    if not hasattr(request.state, "user_id") or request.state.user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

def verify_admin(request: Request):
    if request.state.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied: admin only")

def verify_technician(request: Request):
    if request.state.role != "tecnico":
        raise HTTPException(status_code=403, detail="Access denied: technician only")

def verify_nurse(request: Request):
    if request.state.role != "enfermeiro":
        raise HTTPException(status_code=403, detail="Access denied: nurse only")

async def verify_jwt_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT não fornecido")

    try:
        payload = decode_access_token(token.split(" ")[1])
        request.state.user_id = payload.get("sub")
        request.state.role = payload.get("role")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token JWT inválido")