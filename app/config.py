import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import field_validator, Field
import torch

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # Название модели DeepSeek
    MODEL_NAME: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

    # Кэш для модели
    CACHE_DIR: Path = Field(default=BASE_DIR / "data" / "cached_dir")

    # Девайс
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

    # Директория логов
    LOG_DIR: Path = Field(default=BASE_DIR / "logs")

    # Логирование
    LOG_LEVEL: str = "INFO"
    
    # Публичная ссылка на интерфейс
    SHARE_LINK: bool = False

    @field_validator("CACHE_DIR", "LOG_DIR", mode="before")
    @classmethod
    def validate_paths(cls, value: str) -> Path:
        path = Path(value)
        path.mkdir(parents=True, exist_ok=True)
        return path

    class Config:
        env_file = os.path.join(BASE_DIR.parent.parent, "docker", ".env")

# Экземпляр
settings = Settings()