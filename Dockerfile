FROM python:3.12-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md ./
RUN pip install --no-cache-dir uv && uv sync --locked --no-install-project --no-dev

COPY src/ src/
RUN uv sync --locked --no-dev


FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home appuser
COPY --from=builder --chown=appuser:appuser /app/.venv .venv
COPY --chown=appuser:appuser src/ src/

USER appuser
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["dev"]
