from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.database import db
from app.logging import get_logger, setup_logging
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
log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
  await db.connect()
  log.info("Connected to the Database")
  app.state.db = db
  try:
    yield
  finally:
    await db.close()


app = FastAPI(lifespan=lifespan, title=settings.service_name)

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
