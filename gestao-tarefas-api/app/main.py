"""Ponto de entrada da aplicacao FastAPI."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

# VOLTE A USAR 'from app.'
from app.config import get_settings
from database import engine, create_tables
from app.schemas import HealthResponse, MessageResponse
from app.routes import turmas, alunos, disciplinas, professores, tarefas

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicacao."""
    print("🚀 Iniciando aplicacao...")
    create_tables()
    print("✅ Tabelas criadas/verificadas")
    yield
    print("👋 Encerrando aplicacao...")

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None
)

# CORS para permitir acesso do app da turma de ADS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.is_development else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(turmas.router, prefix="/api/v1")
app.include_router(alunos.router, prefix="/api/v1")
app.include_router(disciplinas.router, prefix="/api/v1")
app.include_router(professores.router, prefix="/api/v1")
app.include_router(tarefas.router, prefix="/api/v1")

@app.get("/", response_model=MessageResponse, tags=["Root"])
def root():
    """Raiz da API."""
    return {
        "message": settings.api_title,
        "detail": f"Versao {settings.api_version} - Acesse /docs para documentacao"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Verifica saude da API e conexao com o banco."""
    try:
        # Testa conexao com o banco
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}