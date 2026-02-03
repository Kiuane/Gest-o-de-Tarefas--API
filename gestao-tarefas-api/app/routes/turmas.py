"""Rotas CRUD para Turmas."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from app.models import Turma
from app.schemas import TurmaCreate, TurmaResponse, MessageResponse

router = APIRouter(prefix="/turmas", tags=["Turmas"])

@router.post("/", response_model=TurmaResponse, status_code=status.HTTP_201_CREATED)
def create_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    """Cria uma nova turma."""
    db_turma = Turma(nome=turma.nome)
    db.add(db_turma)
    try:
        db.commit()
        db.refresh(db_turma)
        return db_turma
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar turma")

@router.get("/", response_model=list[TurmaResponse])
def list_turmas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as turmas."""
    return db.query(Turma).offset(skip).limit(limit).all()

@router.get("/{turma_id}", response_model=TurmaResponse)
def get_turma(turma_id: UUID, db: Session = Depends(get_db)):
    """Busca uma turma pelo ID."""
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma

@router.put("/{turma_id}", response_model=TurmaResponse)
def update_turma(turma_id: UUID, turma_data: TurmaCreate, db: Session = Depends(get_db)):
    """Atualiza uma turma."""
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    turma.nome = turma_data.nome
    db.commit()
    db.refresh(turma)
    return turma

@router.delete("/{turma_id}", response_model=MessageResponse)
def delete_turma(turma_id: UUID, db: Session = Depends(get_db)):
    """Remove uma turma."""
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    db.delete(turma)
    db.commit()
    return {"message": "Turma removida com sucesso", "detail": f"ID: {turma_id}"}