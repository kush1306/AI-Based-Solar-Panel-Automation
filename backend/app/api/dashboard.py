from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.dashboard import DashboardCharts, DashboardOverview
from app.services.dashboard_service import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardOverview)
async def get_dashboard_overview(db: Session = Depends(get_db)):
    return dashboard_service.get_overview(db)


@router.get("/charts", response_model=DashboardCharts)
async def get_dashboard_charts(
    db: Session = Depends(get_db),
    hours: int = Query(24, ge=1, le=168, description="History window in hours"),
):
    return dashboard_service.get_charts(db, hours=hours)
