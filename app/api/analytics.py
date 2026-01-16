from fastapi import APIRouter, Depends
from datetime import date
from typing import List
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.repositories.schedule import ShiftRepository
from app.schemas.analytics import AnalyticsBase
from app.services.analytics import AnalyticsService

router = APIRouter()

def get_analytics_service(db_session: Session = Depends(get_db)) -> AnalyticsService: # however you already obtain a session
    shift_repo = ShiftRepository(db=db_session)
    return AnalyticsService(shift_repo=shift_repo)

@router.get("", response_model=List[AnalyticsBase])
def get_analytics(
    period: str = "day",
    ref_date: date = date.today(),
    service: AnalyticsService = Depends(get_analytics_service),
):
    return service.get_employee_analytics(period=period, ref_date=ref_date)
