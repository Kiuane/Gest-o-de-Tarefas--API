"""
Módulo de autenticação e autorização JWT.
Contém funções para hash de senha, criação/validação de tokens e dependências de segurança.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import get_settings
from database import get_db
from app.models import Aluno
from app.schemas import TokenData

# Configurações
settings = get_settings()

# Contexto para hash de senha usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para Bearer token (JWT)
# tokenUrl é o endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado.
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash bcrypt da senha
        
    Returns:
        True se a senha corresponder, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera hash bcrypt de uma senha.
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash bcrypt da senha
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT de acesso.
    
    Args:
        data: Dados a serem codificados no token (ex: {"sub": email})
        expires_delta: Tempo de expiração personalizado (opcional)
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    # Define a expiração
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    # Adiciona claims ao token
    to_encode.update({
        "exp": expire,  # Expiração
        "iat": datetime.utcnow(),  # Emitido em
        "type": "access"  # Tipo do token
    })
    
    # Codifica o token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decodifica e valida um token JWT.
    
    Args:
        token: Token JWT
        
    Returns:
        Payload decodificado ou None se inválido
    """
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None


async def get_current_aluno(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Aluno:
    """
    Dependência FastAPI que obtém o aluno atual a partir do token JWT.
    Usada para proteger endpoints.
    
    Args:
        token: Token JWT do header Authorization
        db: Sessão do banco de dados
        
    Returns:
        Objeto Aluno autenticado
        
    Raises:
        HTTPException: 401 se token inválido ou aluno não encontrado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodifica o token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extrai o email do subject (sub)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    # Valida expiração explicitamente (redundante mas seguro)
    exp = payload.get("exp")
    if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Busca o aluno no banco
    token_data = TokenData(email=email)
    aluno = db.query(Aluno).filter(Aluno.email == token_data.email).first()
    
    if aluno is None:
        raise credentials_exception
    
    # Verifica se o aluno está ativo (se tiver campo is_active)
    # if hasattr(aluno, 'is_active') and not aluno.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Usuário inativo"
    #     )
    
    return aluno


async def get_current_active_aluno(
    current_aluno: Aluno = Depends(get_current_aluno)
) -> Aluno:
    """
    Versão estendida que verifica se o aluno está ativo.
    (Para usar quando implementar soft delete/desativação)
    """
    # if not current_aluno.is_active:
    #     raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_aluno


def authenticate_aluno(db: Session, email: str, password: str) -> Optional[Aluno]:
    """
    Autentica um aluno verificando email e senha.
    
    Args:
        db: Sessão do banco de dados
        email: Email do aluno
        password: Senha em texto plano
        
    Returns:
        Aluno autenticado ou None se falhar
    """
    aluno = db.query(Aluno).filter(Aluno.email == email).first()
    
    if not aluno:
        return None
    
    if not verify_password(password, aluno.senha_hash):
        return None
    
    return aluno