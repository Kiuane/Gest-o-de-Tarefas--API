"""Modelos SQLAlchemy - Tabelas do DER."""
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, DateTime, ForeignKey, Enum, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base

# Enums
class TipoTarefa(str, PyEnum):
    ATIVIDADE = "ATIVIDADE"
    PROJETO = "PROJETO"

class StatusTarefa(str, PyEnum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"

# ============ TABELA: TURMA ============
class Turma(Base):
    __tablename__ = "turmas"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    alunos: Mapped[list["Aluno"]] = relationship("Aluno", back_populates="turma")

# ============ TABELA: ALUNO ============
class Aluno(Base):
    __tablename__ = "alunos"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    turma_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("turmas.id"), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    # Relacionamentos
    turma: Mapped["Turma"] = relationship("Turma", back_populates="alunos")
    tarefas: Mapped[list["Tarefa"]] = relationship("Tarefa", back_populates="aluno")

# ============ TABELA: DISCIPLINA ============
class Disciplina(Base):
    __tablename__ = "disciplinas"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    professores: Mapped[list["Professor"]] = relationship(
        "Professor", 
        secondary="professor_disciplina",
        back_populates="disciplinas"
    )
    tarefas: Mapped[list["Tarefa"]] = relationship("Tarefa", back_populates="disciplina")

# ============ TABELA: PROFESSOR ============
class Professor(Base):
    __tablename__ = "professores"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    disciplinas: Mapped[list["Disciplina"]] = relationship(
        "Disciplina",
        secondary="professor_disciplina",
        back_populates="professores"
    )
    tarefas: Mapped[list["Tarefa"]] = relationship("Tarefa", back_populates="professor")

# ============ TABELA: PROFESSOR_DISCIPLINA (N:N) ============
class ProfessorDisciplina(Base):
    __tablename__ = "professor_disciplina"
    
    professor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professores.id"), 
        primary_key=True
    )
    disciplina_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("disciplinas.id"), 
        primary_key=True
    )

# ============ TABELA: TAREFA ============
class Tarefa(Base):
    __tablename__ = "tarefas"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aluno_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("alunos.id"), nullable=False)
    tipo: Mapped[TipoTarefa] = mapped_column(Enum(TipoTarefa), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    disciplina_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("disciplinas.id"), nullable=False)
    professor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("professores.id"), nullable=False)
    pontos: Mapped[int] = mapped_column(Integer, nullable=False)
    data_entrega: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[StatusTarefa] = mapped_column(Enum(StatusTarefa), default=StatusTarefa.PENDENTE)
    iniciada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    concluida_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    criada_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relacionamentos
    aluno: Mapped["Aluno"] = relationship("Aluno", back_populates="tarefas")
    disciplina: Mapped["Disciplina"] = relationship("Disciplina", back_populates="tarefas")
    professor: Mapped["Professor"] = relationship("Professor", back_populates="tarefas")