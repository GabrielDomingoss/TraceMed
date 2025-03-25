from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from utils.auth import decode_token
from jwt import PyJWTError

class VerifyJWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ignora rotas públicas (ex: /login)
        if request.url.path.startswith("/api/login"):
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token JWT não fornecido")

        try:
            payload = decode_token(token.split(" ")[1])
            request.state.user_id = payload.get("sub")
            request.state.role = payload.get("role")
        except PyJWTError:
            raise HTTPException(status_code=401, detail="Token JWT inválido")

        return await call_next(request)

# Funções auxiliares de permissão

def verify_admin(request: Request):
    if request.state.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied: admin only")

def verify_technician(request: Request):
    if request.state.role != "tecnico":
        raise HTTPException(status_code=403, detail="Access denied: technician only")

def verify_nurse(request: Request):
    if request.state.role != "enfermeiro":
        raise HTTPException(status_code=403, detail="Access denied: nurse only")
