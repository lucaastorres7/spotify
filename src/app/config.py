from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  service_name: str = "app"
  env: str = "dev"
  version: str = "0.0.1"
  log_level: str = "INFO"

  model_config = {
    "env_file": ".env",
    "env_file_encoding": "utf-8",
  }


settings = Settings()
