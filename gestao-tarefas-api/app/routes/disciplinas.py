"""Rotas CRUD para Disciplinas."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models import Disciplina
from app.schemas import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse, MessageResponse

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

@router.post("/", response_model=DisciplinaResponse, status_code=status.HTTP_201_CREATED)
def create_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    """Cria uma nova disciplina."""
    db_disciplina = Disciplina(nome=disciplina.nome, codigo=disciplina.codigo)
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

@router.get("/", response_model=list[DisciplinaResponse])
def list_disciplinas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as disciplinas."""
    return db.query(Disciplina).offset(skip).limit(limit).all()

@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def get_disciplina(disciplina_id: UUID, db: Session = Depends(get_db)):
    """Busca uma disciplina pelo ID."""
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

@router.put("/{disciplina_id}", response_model=DisciplinaResponse)
def update_disciplina(disciplina_id: UUID, disciplina_data: DisciplinaUpdate, db: Session = Depends(get_db)):
    """Atualiza uma disciplina."""
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    for field, value in disciplina_data.model_dump(exclude_unset=True).items():
        setattr(disciplina, field, value)
    
    db.commit()
    db.refresh(disciplina)
    return disciplina

@router.delete("/{disciplina_id}", response_model=MessageResponse)
def delete_disciplina(disciplina_id: UUID, db: Session = Depends(get_db)):
    """Remove uma disciplina."""
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    db.delete(disciplina)
    db.commit()
    return {"message": "Disciplina removida com sucesso", "detail": f"ID: {disciplina_id}"}