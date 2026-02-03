# Dockerfile com UV para gerenciamento de dependencias
FROM python:3.13-slim

# Metadados
LABEL maintainer="sua-equipe@universidade.edu"
LABEL description="API de Gestao de Tarefas com FastAPI + UV"

# Variaveis de ambiente Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar UV
RUN pip install --no-cache-dir uv

# Diretorio de trabalho
WORKDIR /app

# Instalar dependencias do sistema para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar TUDO para /app
COPY . .

# Instalar dependencias do pyproject.toml (sem instalar o pacote em si)
RUN uv pip install --system fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings python-dotenv passlib email-validator python-multipart

# Expor porta
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para iniciar aplicacao
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]