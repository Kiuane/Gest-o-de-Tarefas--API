"""Rotas CRUD para Alunos."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from database import get_db
from app.models import Aluno
from app.schemas import AlunoCreate, AlunoUpdate, AlunoResponse, MessageResponse

router = APIRouter(prefix="/alunos", tags=["Alunos"])

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def create_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    """Cria um novo aluno."""
    db_aluno = Aluno(
        nome=aluno.nome,
        email=aluno.email,
        senha_hash=hash_password(aluno.password),
        turma_id=aluno.turma_id
    )
    db.add(db_aluno)
    try:
        db.commit()
        db.refresh(db_aluno)
        return db_aluno
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email já cadastrado")

@router.get("/", response_model=list[AlunoResponse])
def list_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os alunos."""
    return db.query(Aluno).offset(skip).limit(limit).all()

@router.get("/{aluno_id}", response_model=AlunoResponse)
def get_aluno(aluno_id: UUID, db: Session = Depends(get_db)):
    """Busca um aluno pelo ID."""
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.put("/{aluno_id}", response_model=AlunoResponse)
def update_aluno(aluno_id: UUID, aluno_data: AlunoUpdate, db: Session = Depends(get_db)):
    """Atualiza um aluno."""
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    update_data = aluno_data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["senha_hash"] = hash_password(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(aluno, field, value)
    
    db.commit()
    db.refresh(aluno)
    return aluno

@router.delete("/{aluno_id}", response_model=MessageResponse)
def delete_aluno(aluno_id: UUID, db: Session = Depends(get_db)):
    """Remove um aluno."""
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return {"message": "Aluno removido com sucesso", "detail": f"ID: {aluno_id}"}