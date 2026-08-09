from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  service_name: str = "app"
  env: str = "dev"
  version: str = "0.0.1"
  log_level: str = "INFO"
  database_url: str = "postgresql+asyncpg://user:password@localhost:5432/db"
  db_pool_size: int = 10

  model_config = {
    "env_file": ".env",
    "env_file_encoding": "utf-8",
    "extra": "ignore",
  }


settings = Settings()
