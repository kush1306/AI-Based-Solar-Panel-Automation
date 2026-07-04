from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Liveness check with optional database connectivity status."""
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "disconnected"

    return {
        "status": "healthy",
        "database": db_status,
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check — verifies MySQL connectivity (for deployment health probes)."""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected",
            "service": settings.app_name,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "database": "disconnected",
                "service": settings.app_name,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
