import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

class LoggingConfig:
    log_level: str = "ERROR"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    log_file: str = "logs/app.log"
    max_bytes = 10 * 1024 * 1024
    backup_count: int = 5

    @classmethod
    def setup(cls, log_level: Optional[str] = None, log_file: Optional[str] = None):
        level = getattr(logging, (log_level or cls.log_level).upper(), logging.ERROR)
        file_path = log_file or cls.log_file

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            fmt=cls.log_format,
            datefmt=cls.log_date_format
        )

        # Настройка корневого логгера
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.handlers.clear()

        file_handler = RotatingFileHandler(
            filename=file_path,
            maxBytes=cls.max_bytes,
            backupCount=cls.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Консольный обработчик
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        logging.getLogger('uvicorn').setLevel(logging.WARNING)
        logging.getLogger('fastapi').setLevel(logging.WARNING)

        return root_logger