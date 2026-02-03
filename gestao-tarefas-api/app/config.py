"""Configurações da aplicação usando Pydantic Settings."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configurações da aplicação."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Banco de Dados
    database_url: str = "postgresql://postgres:postgres@db:5432/gestao_tarefas_db"
    
    # Aplicação
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-in-production"
    
    # API
    api_title: str = "API de Gestão de Tarefas Escolares"
    api_description: str = "API REST para gestão de tarefas, alunos, turmas e disciplinas"
    api_version: str = "1.0.0"
    
    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

@lru_cache
def get_settings() -> Settings:
    return Settings()