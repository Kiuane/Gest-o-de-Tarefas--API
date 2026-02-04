# API de Gestão de Tarefas Escolares

Uma API REST completa para gerenciar tarefas, alunos, turmas, disciplinas e professores em ambientes acadêmicos.

## 🚀 Tecnologias Utilizadas

- **Python** 3.11+
- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para acesso ao banco de dados
- **Pydantic** - Validação de dados
- **PostgreSQL** - Banco de dados relacional
- **Docker Compose** - Orquestração de containers
- **Uvicorn** - Servidor ASGI
- **JWT** - Autenticação via tokens
- **Passlib + Bcrypt** - Hash seguro de senhas

## 📋 Requisitos

- Docker e Docker Compose instalados
- Ou: Python 3.11+ + PostgreSQL local

## 🏃 Como Executar

### Opção 1: Com Docker Compose (Recomendado)

```bash
# Subir a aplicação e banco de dados
docker compose up --build

# Em outro terminal, popular o banco com dados de teste
docker compose exec api python seeds.py --force
```

A API estará disponível em: `http://localhost:8000`

### Opção 2: Localmente (sem Docker)

```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\Activate.ps1

# Instalar dependências
pip install --no-cache-dir \
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

# Ajustar .env para apontar para localhost
# DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/gestao_tarefas_db

# Rodar a aplicação
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000

# Em outro terminal, popular o banco
python seeds.py --force
```

## 📚 Documentação da API

### Swagger UI (Interativo)

Acesse a documentação interativa em:
```
http://localhost:8000/docs
```

### ReDoc (Alternativo)

Acesse a documentação em formato ReDoc em:
```
http://localhost:8000/redoc
```

## 🔑 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação.

### Login

**Endpoint:** `POST /api/v1/auth/login`

**Credenciais de Teste (após rodar seeds):**
- Email: `ana.silva@email.com`
- Senha: `senha123`

**Exemplo de requisição:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ana.silva@email.com&password=senha123"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usar Token em Requisições

Adicione o token no header `Authorization`:
```bash
curl -X GET "http://localhost:8000/api/v1/alunos" \
  -H "Authorization: Bearer <seu_token_aqui>"
```

## 🛣️ Endpoints Principais

### Root
- `GET /` - Informações gerais da API
- `GET /health` - Status de saúde e conexão com banco

### Autenticação
- `POST /api/v1/auth/login` - Fazer login e obter JWT

### Turmas
- `GET /api/v1/turmas` - Listar turmas
- `POST /api/v1/turmas` - Criar turma
- `GET /api/v1/turmas/{id}` - Obter turma por ID
- `PUT /api/v1/turmas/{id}` - Atualizar turma
- `DELETE /api/v1/turmas/{id}` - Deletar turma

### Alunos
- `GET /api/v1/alunos` - Listar alunos
- `POST /api/v1/alunos` - Criar aluno
- `GET /api/v1/alunos/{id}` - Obter aluno por ID
- `PUT /api/v1/alunos/{id}` - Atualizar aluno
- `DELETE /api/v1/alunos/{id}` - Deletar aluno

### Disciplinas
- `GET /api/v1/disciplinas` - Listar disciplinas
- `POST /api/v1/disciplinas` - Criar disciplina
- `GET /api/v1/disciplinas/{id}` - Obter disciplina por ID
- `PUT /api/v1/disciplinas/{id}` - Atualizar disciplina
- `DELETE /api/v1/disciplinas/{id}` - Deletar disciplina

### Professores
- `GET /api/v1/professores` - Listar professores
- `POST /api/v1/professores` - Criar professor
- `GET /api/v1/professores/{id}` - Obter professor por ID
- `PUT /api/v1/professores/{id}` - Atualizar professor
- `DELETE /api/v1/professores/{id}` - Deletar professor

### Tarefas
- `GET /api/v1/tarefas` - Listar tarefas
- `POST /api/v1/tarefas` - Criar tarefa
- `GET /api/v1/tarefas/{id}` - Obter tarefa por ID
- `PUT /api/v1/tarefas/{id}` - Atualizar tarefa
- `DELETE /api/v1/tarefas/{id}` - Deletar tarefa

### Admin
- `POST /admin/seeds` - Executar seeds (dados iniciais)

## 🌱 Dados Iniciais (Seeds)

O projeto inclui um script de seeds que popula o banco com dados fictícios de teste:

**10 alunos** em diferentes turmas
**6 disciplinas** acadêmicas
**6 professores** vinculados às disciplinas
**14 tarefas** com diferentes tipos e status

### Rodar Seeds

```bash
# Com Docker
docker compose exec api python seeds.py --force

# Localmente
python seeds.py --force
```

## 📂 Estrutura do Projeto

```
gestao-tarefas-api/
├── app/
│   ├── app.py           # Aplicação FastAPI principal
│   ├── config.py        # Configurações (settings)
│   ├── models.py        # Modelos SQLAlchemy
│   ├── schemas.py       # Schemas Pydantic para validação
│   └── routes/
│       ├── auth.py      # Rotas de autenticação
│       ├── alunos.py    # Rotas de alunos
│       ├── turmas.py    # Rotas de turmas
│       ├── disciplinas.py
│       ├── professores.py
│       └── tarefas.py   # Rotas de tarefas
├── auth.py              # Lógica de JWT e autenticação
├── database.py          # Configuração do banco de dados
├── seeds.py             # Script para popular dados iniciais
├── docker-compose.yml   # Orquestração Docker
├── Dockerfile           # Imagem Docker da aplicação
├── pyproject.toml       # Configuração do projeto (Python)
├── .env                 # Variáveis de ambiente
└── README.md            # Este arquivo
```

## 🔐 Segurança

- Senhas são criptografadas com **bcrypt**
- Tokens JWT com expiração configurável
- CORS habilitado para desenvolvimento
- Validação de dados em tempo real com Pydantic

## 🧪 Teste de Login

Para testar o endpoint de login rapidamente:

```bash
python scripts/test_login.py
```

## 🛠️ Desenvolvimento

### Adicionar Novas Dependências

Editar `pyproject.toml` e reconstruir a imagem Docker:

```bash
docker compose down
docker compose up --build
```

### Variáveis de Ambiente

As principais variáveis de ambiente estão em `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres123@db:5432/gestao_tarefas_db
APP_ENV=development
DEBUG=true
SECRET_KEY=dev_secret_key_change_in_production
```

## 📞 Contato

Para dúvidas ou sugestões sobre a API, entre em contato com a equipe de desenvolvimento.

---

**Versão:** 1.0.0  
**Data:** Fevereiro de 2026
