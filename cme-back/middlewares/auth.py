from fastapi import Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from config import SECRET_KEY, ALGORITHM
from models.user import User
from database import SessionLocal

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json") or request.url.path.startswith("/api/users/login"):
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token de autenticação não fornecido")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token inválido")
        except JWTError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token inválido")

        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()

        if not user:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

        request.state.user = user
        response = await call_next(request)
        return response
