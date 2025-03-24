from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from middlewares.auth import AuthMiddleware
from middlewares.permissions import RoleMiddleware
from middlewares.auth import verify_jwt_token
from routes import (
    user_routes, material_routes, process_routes,
    failure_routes, etapa_routes, report_routes
)
import database

app = FastAPI(title="TraceMed API")


app.add_middleware(AuthMiddleware)
app.add_middleware(RoleMiddleware)
app.add_middleware("http")(verify_jwt_token)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# conectando ao banco de dados
database.connect()

# incluindo as rotas
app.include_router(user_routes.router, prefix="/api/users", tags=["Usuários"])
app.include_router(material_routes.router, prefix="/api/materials", tags=["Materials"])
app.include_router(process_routes.router, prefix="/api/processes", tags=["Processes"])
app.include_router(failure_routes.router, prefix="/api/failures", tags=["Failures"])
app.include_router(etapa_routes.router, prefix="/api/etapas", tags=["Etapas"])
app.include_router(report_routes.router, prefix="/api/reports", tags=["Reports"])


