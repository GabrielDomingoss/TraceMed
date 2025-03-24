from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM
from database import SessionLocal
from models.user import User

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):  # Protege todas as rotas da API
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Token JWT não fornecido")

            token = token.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get("sub")
                if user_id is None:
                    raise HTTPException(status_code=401, detail="Token inválido")
            except JWTError:
                raise HTTPException(status_code=401, detail="Token inválido")

            # Carregar o usuário do banco de dados
            db = SessionLocal()
            user = db.query(User).filter(User.id == int(user_id)).first()
            db.close()
            if not user:
                raise HTTPException(status_code=401, detail="Usuário não encontrado")

            # Adicionar informações do usuário ao estado da requisição
            request.state.user_id = user.id
            request.state.role = user.role

        return await call_next(request)
