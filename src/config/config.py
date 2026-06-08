from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_NAMESPACE: str = ""
    API_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding='utf-8', extra='ignore')


def get_settings():
    return Settings()