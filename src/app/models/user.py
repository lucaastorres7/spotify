import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, String

from app.models import Base


def get_uct() -> datetime:
  return datetime.now(UTC)


class User(Base):
  __tablename__ = "users"

  id = Column(String, primary_key=True, default=uuid.uuid4())
  email = Column(String, unique=True, nullable=False)
  username = Column(String, nullable=False)
  created_at = Column(DateTime(timezone=True), default=get_uct(), nullable=False)
  updated_at = Column(
    DateTime(timezone=True), default=get_uct(), onupdate=get_uct(), nullable=False
  )
