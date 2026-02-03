"""Rotas CRUD para Professores."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from app.models import Professor, Disciplina, ProfessorDisciplina
from app.schemas import (
    ProfessorCreate, ProfessorUpdate, ProfessorResponse, 
    ProfessorDisciplinaCreate, MessageResponse
)

router = APIRouter(prefix="/professores", tags=["Professores"])

@router.post("/", response_model=ProfessorResponse, status_code=status.HTTP_201_CREATED)
def create_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    """Cria um novo professor."""
    db_professor = Professor(nome=professor.nome, email=professor.email)
    db.add(db_professor)
    try:
        db.commit()
        db.refresh(db_professor)
        return db_professor
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email já cadastrado")

@router.get("/", response_model=list[ProfessorResponse])
def list_professores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os professores."""
    return db.query(Professor).offset(skip).limit(limit).all()

@router.get("/{professor_id}", response_model=ProfessorResponse)
def get_professor(professor_id: UUID, db: Session = Depends(get_db)):
    """Busca um professor pelo ID."""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return professor

@router.put("/{professor_id}", response_model=ProfessorResponse)
def update_professor(professor_id: UUID, professor_data: ProfessorUpdate, db: Session = Depends(get_db)):
    """Atualiza um professor."""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    for field, value in professor_data.model_dump(exclude_unset=True).items():
        setattr(professor, field, value)
    
    db.commit()
    db.refresh(professor)
    return professor

@router.delete("/{professor_id}", response_model=MessageResponse)
def delete_professor(professor_id: UUID, db: Session = Depends(get_db)):
    """Remove um professor."""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    db.delete(professor)
    db.commit()
    return {"message": "Professor removido com sucesso", "detail": f"ID: {professor_id}"}

@router.post("/{professor_id}/disciplinas/{disciplina_id}", response_model=MessageResponse)
def vincular_disciplina(professor_id: UUID, disciplina_id: UUID, db: Session = Depends(get_db)):
    """Vincula um professor a uma disciplina."""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    
    if not professor or not disciplina:
        raise HTTPException(status_code=404, detail="Professor ou disciplina não encontrados")
    
    vinculo = ProfessorDisciplina(professor_id=professor_id, disciplina_id=disciplina_id)
    db.add(vinculo)
    db.commit()
    return {"message": "Professor vinculado à disciplina com sucesso"}