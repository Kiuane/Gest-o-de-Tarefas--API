"""Rotas CRUD para Tarefas."""
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models import Tarefa, StatusTarefa
from app.schemas import TarefaCreate, TarefaUpdate, TarefaResponse, MessageResponse

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])

@router.post("/", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def create_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    """Cria uma nova tarefa."""
    db_tarefa = Tarefa(**tarefa.model_dump())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

@router.get("/", response_model=list[TarefaResponse])
def list_tarefas(
    skip: int = 0, 
    limit: int = 100, 
    aluno_id: UUID | None = None,
    status: StatusTarefa | None = None,
    db: Session = Depends(get_db)
):
    """Lista tarefas com filtros opcionais."""
    query = db.query(Tarefa)
    if aluno_id:
        query = query.filter(Tarefa.aluno_id == aluno_id)
    if status:
        query = query.filter(Tarefa.status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/{tarefa_id}", response_model=TarefaResponse)
def get_tarefa(tarefa_id: UUID, db: Session = Depends(get_db)):
    """Busca uma tarefa pelo ID."""
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@router.put("/{tarefa_id}", response_model=TarefaResponse)
def update_tarefa(tarefa_id: UUID, tarefa_data: TarefaUpdate, db: Session = Depends(get_db)):
    """Atualiza uma tarefa."""
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    update_data = tarefa_data.model_dump(exclude_unset=True)
    
    # Atualizar timestamps de status
    if "status" in update_data:
        if update_data["status"] == StatusTarefa.EM_ANDAMENTO and not tarefa.iniciada_em:
            update_data["iniciada_em"] = datetime.now()
        elif update_data["status"] == StatusTarefa.CONCLUIDA and not tarefa.concluida_em:
            update_data["concluida_em"] = datetime.now()
    
    for field, value in update_data.items():
        setattr(tarefa, field, value)
    
    db.commit()
    db.refresh(tarefa)
    return tarefa

@router.delete("/{tarefa_id}", response_model=MessageResponse)
def delete_tarefa(tarefa_id: UUID, db: Session = Depends(get_db)):
    """Remove uma tarefa."""
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"message": "Tarefa removida com sucesso", "detail": f"ID: {tarefa_id}"}