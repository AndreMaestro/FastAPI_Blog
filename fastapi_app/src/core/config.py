from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8'
    )

    PORT: int = 8000
    HOST: str = "127.0.0.1"
    ROOT_PATH: str = ''
    RELOAD: bool = False

    ORIGINS: str = "*"  # значение по умолчанию

    DATABASE_URL: str = "sqlite:///./db.sqlite3"

    SECRET_AUTH_KEY: SecretStr

    IMAGE_DIR: str = "image"
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024

    LOG_LEVEL: str = "ERROR"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024
    LOG_BACKUP_COUNT: int = 5


settings = Settings()