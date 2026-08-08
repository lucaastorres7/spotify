import logging
import sys

import structlog

from .processors import build_service_context_processor

get_logger = structlog.get_logger


def setup_logging(
  service: str, level: str = "INFO", fmt: str = "console", env: str = "-", version: str = "-"
) -> None:

  level = level
  fmt = fmt

  shared_processors: list = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    build_service_context_processor(service, env, version),
    structlog.processors.StackInfoRenderer(),
  ]

  if fmt == "json":
    shared_processors.append(structlog.processors.format_exc_info)
    renderer = structlog.processors.JSONRenderer()
  else:
    renderer = structlog.dev.ConsoleRenderer(colors=True)

  # --- structlog (logs emitidos via get_logger) ---
  structlog.configure(
    processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
  )

  # --- stdlib (logs de uvicorn, gunicorn, libs de terceiros) ---
  formatter = structlog.stdlib.ProcessorFormatter(
    foreign_pre_chain=shared_processors,
    processors=[
      structlog.stdlib.ProcessorFormatter.remove_processors_meta,
      renderer,
    ],
  )

  handler = logging.StreamHandler(sys.stdout)  # 12-factor: stdout, coletor cuida do resto
  handler.setFormatter(formatter)

  root = logging.getLogger()
  root.handlers.clear()
  root.addHandler(handler)
  root.setLevel(level)


__all__ = ["setup_logging", "get_logger"]
