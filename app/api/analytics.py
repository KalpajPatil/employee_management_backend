from fastapi import APIRouter, Depends
from datetime import date
from typing import List
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.repositories.schedule import ShiftRepository
from app.schemas.analytics import AnalyticsBase
from app.services.analytics import AnalyticsService

router = APIRouter()

def get_analytics_service(db_session: Session = Depends(get_db)) -> AnalyticsService:
    shift_repo = ShiftRepository(db=db_session)
    return AnalyticsService(shift_repo=shift_repo)

#get all employee analytics and by date
@router.get("", response_model=List[AnalyticsBase])
def get_analytics(
    period: str | None = None,
    ref_date: date | None = None,
    service: AnalyticsService = Depends(get_analytics_service),
):
    return service.get_employee_analytics(period=period, ref_date=ref_date)

#get employee analytics by employee id
@router.get("/{employee_id}", response_model=List[AnalyticsBase])
def get_employee_analytics(
    employee_id: int,
    period: str | None = None,
    ref_date: date | None = None,
    service: AnalyticsService = Depends(get_analytics_service),
):
    all_rows = service.get_employee_analytics(period=period, ref_date=ref_date)
    return [row for row in all_rows if row.employee_id == employee_id]
