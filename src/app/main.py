import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.logging import setup_logging
from app.logging.middleware import RequestContextMiddleware
from app.routes import health_router

# -- Logging setup --
setup_logging(
  service=settings.service_name,
  level=settings.log_level,
  fmt="json" if settings.env == "prod" else "console",
  env=settings.env,
  version=settings.version,
)

app = FastAPI()

# -- Middlewares --
app.add_middleware(RequestContextMiddleware)

# -- Routes --
app.include_router(health_router)


def run():
  uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=settings.env == "dev",
    log_config=None,
    access_log=False,
  )
