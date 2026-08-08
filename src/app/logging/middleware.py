import time
import uuid

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

log = structlog.get_logger("access_logger")


class RequestContextMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
      request_id=request_id,
      method=request.method,
      path=request.url.path,
    )

    start_time = time.perf_counter()

    try:
      response: Response = await call_next(request)

    except Exception:
      duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
      log.exception("request_failed", duration_ms=duration_ms)
      raise

    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    log.info(
      "request_completed",
      status_code=response.status_code,
      duration_ms=duration_ms,
    )

    response.headers["X-Request-ID"] = request_id
    return response
