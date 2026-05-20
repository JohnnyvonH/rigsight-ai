from functools import cached_property

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./rigsight.db"
    backend_cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @computed_field
    @cached_property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]


settings = Settings()
