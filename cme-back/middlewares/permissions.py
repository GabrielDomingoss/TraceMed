from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from database import SessionLocal
from models.user import User
import os

SECRET_KEY = os.getenv("SECRET_KEY", "segredo_super_secreto")
ALGORITHM = "HS256"

class RoleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        route: APIRoute = request.scope.get("route")
        endpoint = route.endpoint if route else None

        # Ignora rotas públicas (login, registro, etc)
        if not endpoint or getattr(endpoint, "public", False):
            return await call_next(request)

        # Extrai o token do cabeçalho
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token ausente ou inválido")

        token = auth.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            role = payload.get("role")
            if user_id is None or role is None:
                raise HTTPException(status_code=401, detail="Token inválido")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

        # Salva no state para uso nos handlers
        request.state.user_id = user_id
        request.state.role = role

        return await call_next(request)
