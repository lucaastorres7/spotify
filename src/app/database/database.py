from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
  AsyncEngine,
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)

from app.config import settings


class Database:
  def __init__(self, url: str, pool_size: int = 5, echo: bool = False):
    self._engine: AsyncEngine = create_async_engine(
      url,
      pool_size=pool_size,
      echo=echo,
      max_overflow=10,
      pool_pre_ping=True,
    )
    self._sessionmaker: AsyncSession = async_sessionmaker(
      self._engine,
      expire_on_commit=False,
      autoflush=False,
    )

  async def connect(self) -> None:
    async with self._engine.connect() as conn:
      await conn.execute(text("SELECT 1"))

  async def get_session(self) -> AsyncSession:
    return self._sessionmaker()

  async def close(self) -> None:
    await self._engine.dispose()


db = Database(url=settings.database_url, pool_size=settings.db_pool_size, echo=False)
