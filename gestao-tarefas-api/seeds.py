"""
Script para popular o banco de dados com dados iniciais (seeds).
Execute: docker compose exec api python -m app.seeds
Ou: python -m app.seeds (se estiver com ambiente local)
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from app.models import Base, Turma, Aluno, Disciplina, Professor, Tarefa, TipoTarefa, StatusTarefa
from auth import get_password_hash


def criar_turmas(db: Session) -> list[Turma]:
    """Cria turmas iniciais."""
    turmas_data = [
        {"nome": "ADS 2025.1 - Manhã"},
        {"nome": "ADS 2025.1 - Noite"},
        {"nome": "ADS 2025.2 - Manhã"},
        {"nome": "ADS 2025.2 - Noite"},
        {"nome": "Engenharia de Software 2025.1"},
        {"nome": "Ciência da Computação 2025.1"},
    ]
    
    turmas = []
    for data in turmas_data:
        turma = Turma(nome=data["nome"])
        db.add(turma)
        turmas.append(turma)
    
    db.commit()
    for turma in turmas:
        db.refresh(turma)
    
    print(f"✅ {len(turmas)} turmas criadas")
    return turmas


def criar_alunos(db: Session, turmas: list[Turma]) -> list[Aluno]:
    """Cria alunos iniciais vinculados às turmas."""
    alunos_data = [
        {"nome": "Ana Silva", "email": "ana.silva@email.com", "senha": "senha123", "turma_index": 0},
        {"nome": "Bruno Santos", "email": "bruno.santos@email.com", "senha": "senha123", "turma_index": 0},
        {"nome": "Carla Oliveira", "email": "carla.oliveira@email.com", "senha": "senha123", "turma_index": 1},
        {"nome": "Daniel Costa", "email": "daniel.costa@email.com", "senha": "senha123", "turma_index": 1},
        {"nome": "Elena Martins", "email": "elena.martins@email.com", "senha": "senha123", "turma_index": 2},
        {"nome": "Felipe Souza", "email": "felipe.souza@email.com", "senha": "senha123", "turma_index": 2},
        {"nome": "Gabriela Lima", "email": "gabriela.lima@email.com", "senha": "senha123", "turma_index": 3},
        {"nome": "Henrique Pereira", "email": "henrique.pereira@email.com", "senha": "senha123", "turma_index": 3},
        {"nome": "Isabela Fernandes", "email": "isabela.fernandes@email.com", "senha": "senha123", "turma_index": 4},
        {"nome": "João Rodrigues", "email": "joao.rodrigues@email.com", "senha": "senha123", "turma_index": 5},
    ]
    
    alunos = []
    for data in alunos_data:
        aluno = Aluno(
            nome=data["nome"],
            email=data["email"],
            senha_hash=get_password_hash(data["senha"]),
            turma_id=turmas[data["turma_index"]].id
        )
        db.add(aluno)
        alunos.append(aluno)
    
    db.commit()
    for aluno in alunos:
        db.refresh(aluno)
    
    print(f"✅ {len(alunos)} alunos criados")
    print("   Emails de acesso:")
    for aluno in alunos:
        print(f"   - {aluno.email} / senha: senha123")
    return alunos


def criar_disciplinas(db: Session) -> list[Disciplina]:
    """Cria disciplinas iniciais."""
    disciplinas_data = [
        {"nome": "Programação Web", "codigo": "PW001"},
        {"nome": "Banco de Dados", "codigo": "BD002"},
        {"nome": "Engenharia de Software", "codigo": "ES003"},
        {"nome": "Estrutura de Dados", "codigo": "ED004"},
        {"nome": "Redes de Computadores", "codigo": "RC005"},
        {"nome": "Sistemas Operacionais", "codigo": "SO006"},
        {"nome": "Inteligência Artificial", "codigo": "IA007"},
        {"nome": "Desenvolvimento Mobile", "codigo": "DM008"},
    ]
    
    disciplinas = []
    for data in disciplinas_data:
        disciplina = Disciplina(
            nome=data["nome"],
            codigo=data["codigo"]
        )
        db.add(disciplina)
        disciplinas.append(disciplina)
    
    db.commit()
    for disciplina in disciplinas:
        db.refresh(disciplina)
    
    print(f"✅ {len(disciplinas)} disciplinas criadas")
    return disciplinas


def criar_professores(db: Session, disciplinas: list[Disciplina]) -> list[Professor]:
    """Cria professores e vincula às disciplinas."""
    professores_data = [
        {"nome": "Prof. Carlos Mendes", "email": "carlos.mendes@universidade.edu", "disciplinas": [0, 1]},
        {"nome": "Profa. Maria Helena", "email": "maria.helena@universidade.edu", "disciplinas": [2, 3]},
        {"nome": "Prof. Roberto Alves", "email": "roberto.alves@universidade.edu", "disciplinas": [4, 5]},
        {"nome": "Profa. Fernanda Costa", "email": "fernanda.costa@universidade.edu", "disciplinas": [6, 7]},
        {"nome": "Prof. Antônio Pereira", "email": "antonio.pereira@universidade.edu", "disciplinas": [0, 3]},
        {"nome": "Profa. Juliana Lima", "email": "juliana.lima@universidade.edu", "disciplinas": [1, 2]},
    ]
    
    professores = []
    for data in professores_data:
        professor = Professor(
            nome=data["nome"],
            email=data["email"]
        )
        # Vincular disciplinas
        for disc_index in data["disciplinas"]:
            professor.disciplinas.append(disciplinas[disc_index])
        
        db.add(professor)
        professores.append(professor)
    
    db.commit()
    for professor in professores:
        db.refresh(professor)
    
    print(f"✅ {len(professores)} professores criados")
    return professores


def criar_tarefas(
    db: Session,
    alunos: list[Aluno],
    disciplinas: list[Disciplina],
    professores: list[Professor]
) -> list[Tarefa]:
    """Cria tarefas iniciais para os alunos."""
    hoje = datetime.utcnow()
    
    tarefas_data = [
        # Aluno 0 - Ana Silva
        {
            "aluno_index": 0,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Lista de Exercícios 01 - HTML/CSS",
            "descricao": "Criar uma página HTML semântica com estilização CSS",
            "disciplina_index": 0,  # Programação Web
            "professor_index": 0,   # Carlos Mendes
            "pontos": 10,
            "data_entrega": hoje + timedelta(days=7),
            "status": StatusTarefa.PENDENTE
        },
        {
            "aluno_index": 0,
            "tipo": TipoTarefa.PROJETO,
            "titulo": "Sistema de Cadastro com Flask",
            "descricao": "Desenvolver um sistema completo de cadastro usando Flask e SQLAlchemy",
            "disciplina_index": 0,  # Programação Web
            "professor_index": 4,   # Antônio Pereira
            "pontos": 30,
            "data_entrega": hoje + timedelta(days=30),
            "status": StatusTarefa.EM_ANDAMENTO,
            "iniciada_em": hoje - timedelta(days=2)
        },
        # Aluno 1 - Bruno Santos
        {
            "aluno_index": 1,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Modelagem ER - Biblioteca",
            "descricao": "Criar diagrama entidade-relacionamento para sistema de biblioteca",
            "disciplina_index": 1,  # Banco de Dados
            "professor_index": 5,   # Juliana Lima
            "pontos": 15,
            "data_entrega": hoje + timedelta(days=5),
            "status": StatusTarefa.CONCLUIDA,
            "iniciada_em": hoje - timedelta(days=5),
            "concluida_em": hoje - timedelta(days=1)
        },
        # Aluno 2 - Carla Oliveira
        {
            "aluno_index": 2,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Caso de Uso - Sistema Acadêmico",
            "descricao": "Elaborar diagrama de casos de uso para sistema acadêmico",
            "disciplina_index": 2,  # Engenharia de Software
            "professor_index": 1,   # Maria Helena
            "pontos": 20,
            "data_entrega": hoje + timedelta(days=10),
            "status": StatusTarefa.PENDENTE
        },
        {
            "aluno_index": 2,
            "tipo": TipoTarefa.PROJETO,
            "titulo": "Documentação de Requisitos",
            "descricao": "Documento completo de requisitos funcionais e não-funcionais",
            "disciplina_index": 2,  # Engenharia de Software
            "professor_index": 1,   # Maria Helena
            "pontos": 40,
            "data_entrega": hoje + timedelta(days=45),
            "status": StatusTarefa.EM_ANDAMENTO,
            "iniciada_em": hoje - timedelta(days=5)
        },
        # Aluno 3 - Daniel Costa
        {
            "aluno_index": 3,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Implementação de Lista Encadeada",
            "descricao": "Implementar lista encadeada em Python com operações CRUD",
            "disciplina_index": 3,  # Estrutura de Dados
            "professor_index": 1,   # Maria Helena
            "pontos": 25,
            "data_entrega": hoje + timedelta(days=3),
            "status": StatusTarefa.EM_ANDAMENTO,
            "iniciada_em": hoje - timedelta(days=1)
        },
        # Aluno 4 - Elena Martins
        {
            "aluno_index": 4,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Configuração de Rede Local",
            "descricao": "Simular configuração de rede com endereçamento IP",
            "disciplina_index": 4,  # Redes de Computadores
            "professor_index": 2,   # Roberto Alves
            "pontos": 15,
            "data_entrega": hoje + timedelta(days=14),
            "status": StatusTarefa.PENDENTE
        },
        {
            "aluno_index": 4,
            "tipo": TipoTarefa.PROJETO,
            "titulo": "Análise de Protocolos",
            "descricao": "Análise de pacotes TCP/IP usando Wireshark",
            "disciplina_index": 4,  # Redes de Computadores
            "professor_index": 2,   # Roberto Alves
            "pontos": 35,
            "data_entrega": hoje + timedelta(days=60),
            "status": StatusTarefa.PENDENTE
        },
        # Aluno 5 - Felipe Souza
        {
            "aluno_index": 5,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Script de Backup em Bash",
            "descricao": "Criar script automatizado de backup usando shell script",
            "disciplina_index": 5,  # Sistemas Operacionais
            "professor_index": 2,   # Roberto Alves
            "pontos": 20,
            "data_entrega": hoje + timedelta(days=7),
            "status": StatusTarefa.CONCLUIDA,
            "iniciada_em": hoje - timedelta(days=3),
            "concluida_em": hoje
        },
        # Aluno 6 - Gabriela Lima
        {
            "aluno_index": 6,
            "tipo": TipoTarefa.PROJETO,
            "titulo": "Chatbot com Python",
            "descricao": "Implementar chatbot simples usando processamento de linguagem natural",
            "disciplina_index": 6,  # Inteligência Artificial
            "professor_index": 3,   # Fernanda Costa
            "pontos": 50,
            "data_entrega": hoje + timedelta(days=90),
            "status": StatusTarefa.EM_ANDAMENTO,
            "iniciada_em": hoje - timedelta(days=10)
        },
        # Aluno 7 - Henrique Pereira
        {
            "aluno_index": 7,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Layout Responsivo",
            "descricao": "Criar layout responsivo para aplicativo mobile",
            "disciplina_index": 7,  # Desenvolvimento Mobile
            "professor_index": 3,   # Fernanda Costa
            "pontos": 20,
            "data_entrega": hoje + timedelta(days=5),
            "status": StatusTarefa.PENDENTE
        },
        # Aluno 8 - Isabela Fernandes
        {
            "aluno_index": 8,
            "tipo": TipoTarefa.ATIVIDADE,
            "titulo": "Normalização de Banco de Dados",
            "descricao": "Aplicar 1FN, 2FN e 3FN em modelo de dados",
            "disciplina_index": 1,  # Banco de Dados
            "professor_index": 5,   # Juliana Lima
            "pontos": 15,
            "data_entrega": hoje + timedelta(days=4),
            "status": StatusTarefa.EM_ANDAMENTO,
            "iniciada_em": hoje - timedelta(days=1)
        },
        # Aluno 9 - João Rodrigues
        {
            "aluno_index": 9,
            "tipo": TipoTarefa.PROJETO,
            "titulo": "Aplicativo de Lista de Tarefas",
            "descricao": "Desenvolver app mobile de lista de tarefas com React Native",
            "disciplina_index": 7,  # Desenvolvimento Mobile
            "professor_index": 3,   # Fernanda Costa
            "pontos": 60,
            "data_entrega": hoje + timedelta(days=120),
            "status": StatusTarefa.PENDENTE
        },
    ]
    
    tarefas = []
    for data in tarefas_data:
        tarefa = Tarefa(
            aluno_id=alunos[data["aluno_index"]].id,
            tipo=data["tipo"],
            titulo=data["titulo"],
            descricao=data["descricao"],
            disciplina_id=disciplinas[data["disciplina_index"]].id,
            professor_id=professores[data["professor_index"]].id,
            pontos=data["pontos"],
            data_entrega=data["data_entrega"],
            status=data["status"],
            iniciada_em=data.get("iniciada_em"),
            concluida_em=data.get("concluida_em")
        )
        db.add(tarefa)
        tarefas.append(tarefa)
    
    db.commit()
    for tarefa in tarefas:
        db.refresh(tarefa)
    
    print(f"✅ {len(tarefas)} tarefas criadas")
    return tarefas


def limpar_banco(db: Session):
    """Limpa todas as tabelas (cuidado!)."""
    print("🧹 Limpando banco de dados...")
    db.query(Tarefa).delete()
    db.query(Aluno).delete()
    db.query(Turma).delete()
    db.query(Professor).delete()
    db.query(Disciplina).delete()
    db.commit()
    print("✅ Banco limpo")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Executa seeds no banco de dados")
    parser.add_argument("--force", action="store_true", help="Ignora prompts e força recriação")
    args = parser.parse_args()

    # Função interna que executa a lógica (para permitir chamada forçada)
    def _run(force: bool = False):
        print("=" * 50)
        print("🌱 SEMENTES DO SISTEMA ACADÊMICO")
        print("=" * 50)

        db = SessionLocal()
        try:
            # Verificar se já existe dados
            if db.query(Turma).first():
                print("⚠️  Banco já contém dados!")
                if force:
                    from app.models import ProfessorDisciplina
                    limpar_banco(db)
                else:
                    resposta = input("Deseja limpar e recriar? (s/N): ")
                    if resposta.lower() == 's':
                        from app.models import ProfessorDisciplina
                        limpar_banco(db)
                    else:
                        print("❌ Operação cancelada")
                        return

            print("\n📚 Criando dados iniciais...\n")

            # Criar dados em ordem (respeitando FKs)
            turmas = criar_turmas(db)
            alunos = criar_alunos(db, turmas)
            disciplinas = criar_disciplinas(db)
            professores = criar_professores(db, disciplinas)
            tarefas = criar_tarefas(db, alunos, disciplinas, professores)

            print("\n" + "=" * 50)
            print("✅ SEEDS CONCLUÍDOS COM SUCESSO!")
            print("=" * 50)
            print(f"\n📊 Resumo:")
            print(f"   • {len(turmas)} turmas")
            print(f"   • {len(alunos)} alunos")
            print(f"   • {len(disciplinas)} disciplinas")
            print(f"   • {len(professores)} professores")
            print(f"   • {len(tarefas)} tarefas")
            print(f"\n🔑 Credenciais de teste:")
            print(f"   Email: ana.silva@email.com")
            print(f"   Senha: senha123")
            print(f"\n   Ou use qualquer email da lista acima com senha: senha123")
            print(f"\n🚀 API disponível em: http://localhost:8000")
            print(f"📖 Documentação: http://localhost:8000/docs")

        except Exception as e:
            print(f"\n❌ Erro: {e}")
            db.rollback()
            raise
        finally:
            db.close()

    _run(force=args.force)


if __name__ == "__main__":
    main()