"""Schemas Pydantic para validação de dados."""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from app.models import TipoTarefa, StatusTarefa

# ============ SCHEMAS: TURMA ============
class TurmaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)

class TurmaCreate(TurmaBase):
    pass

class TurmaResponse(TurmaBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    criada_em: datetime

# ============ SCHEMAS: ALUNO ============
class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    email: EmailStr

class AlunoCreate(AlunoBase):
    password: str = Field(..., min_length=8, max_length=128)
    turma_id: UUID

class AlunoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=255)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=128)
    turma_id: UUID | None = None

class AlunoResponse(AlunoBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    turma_id: UUID
    criado_em: datetime
    atualizado_em: datetime

# ============ SCHEMAS: DISCIPLINA ============
class DisciplinaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    codigo: str | None = Field(None, max_length=50)

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=255)
    codigo: str | None = Field(None, max_length=50)

class DisciplinaResponse(DisciplinaBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    criada_em: datetime

# ============ SCHEMAS: PROFESSOR ============
class ProfessorBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    email: EmailStr | None = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=255)
    email: EmailStr | None = None

class ProfessorResponse(ProfessorBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    criado_em: datetime

# ============ SCHEMAS: PROFESSOR_DISCIPLINA ============
class ProfessorDisciplinaCreate(BaseModel):
    professor_id: UUID
    disciplina_id: UUID

class ProfessorDisciplinaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    professor_id: UUID
    disciplina_id: UUID

# ============ SCHEMAS: TAREFA ============
class TarefaBase(BaseModel):
    tipo: TipoTarefa
    titulo: str = Field(..., min_length=2, max_length=255)
    descricao: str | None = None
    pontos: int = Field(..., ge=0)
    data_entrega: datetime

class TarefaCreate(TarefaBase):
    aluno_id: UUID
    disciplina_id: UUID
    professor_id: UUID

class TarefaUpdate(BaseModel):
    tipo: TipoTarefa | None = None
    titulo: str | None = Field(None, min_length=2, max_length=255)
    descricao: str | None = None
    pontos: int | None = Field(None, ge=0)
    data_entrega: datetime | None = None
    status: StatusTarefa | None = None

class TarefaResponse(TarefaBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    aluno_id: UUID
    disciplina_id: UUID
    professor_id: UUID
    status: StatusTarefa
    iniciada_em: datetime | None
    concluida_em: datetime | None
    criada_em: datetime
    atualizada_em: datetime

# ============ SCHEMAS: MENSAGENS ============
class MessageResponse(BaseModel):
    message: str
    detail: str | None = None

class HealthResponse(BaseModel):
    status: str
    database: str
    environment: str


# ============ SCHEMAS: AUTH/TOKEN ============
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None


class TokenData(BaseModel):
    email: str | None = None