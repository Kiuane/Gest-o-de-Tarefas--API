FROM python:3.11-slim

LABEL maintainer="sua-equipe@universidade.edu"
LABEL description="API de Gestao de Tarefas com FastAPI + UV"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencias do sistema (PostgreSQL + healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Uvicorn e dependências via requirements.txt
RUN pip install --no-cache-dir \
    fastapi>=0.115.0 \
    "uvicorn[standard]>=0.34.0" \
    sqlalchemy>=2.0.36 \
    psycopg2-binary>=2.9.10 \
    pydantic>=2.10.4 \
    pydantic-settings>=2.7.0 \
    python-dotenv>=1.0.1 \
    "passlib[bcrypt]>=1.7.4" \
    "python-jose[cryptography]>=3.3.0" \
    email-validator>=2.2.0 \
    python-multipart>=0.0.20

# Copiar o resto do projeto
COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
