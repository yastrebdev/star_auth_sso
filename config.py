from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///sqlite.db"

    class Config:
        env_file = ".env"


settings = Settings()