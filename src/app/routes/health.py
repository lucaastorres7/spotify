from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
  return JSONResponse(content={"status": "healthy", "env": settings.env}, status_code=200)
