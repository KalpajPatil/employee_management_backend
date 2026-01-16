from datetime import date, timedelta
import logging
from typing import Optional

from app.repositories.schedule import ShiftRepository
from app.schemas.analytics import AnalyticsResponse

logger = logging.getLogger(__name__)
class AnalyticsService:
    def __init__(self, shift_repo: ShiftRepository):
        self.shift_repo = shift_repo

    
    def _get_period_range(self, period: str, ref_date: date):
        if period == "day":
            return ref_date, ref_date

        if period == "week":
            # assuming Monday as first day
            # start will give monday's date
            start = ref_date - timedelta(days=ref_date.weekday())
            
            # end will give sunday's date for that week
            end = start + timedelta(days=6)
            return start, end

        if period == "month":

            # start is now the first day of the current month
            start = ref_date.replace(day=1)
            if start.month == 12:

                # if month is dec, next month is jan of next year
                next_month = start.replace(year=start.year + 1, month=1, day=1)
            else:

                # else just increment the month by 1
                next_month = start.replace(month=start.month + 1, day=1)
            end = next_month - timedelta(days=1)
            return start, end

        raise ValueError("Invalid period; use day, week, or month")

    def get_employee_analytics(self, period: Optional[str], ref_date: Optional[date]):
        logger.info("inside get_employee_analytics")
        if period is None and ref_date is None:
            logger.info("inside if")
            rows = self.shift_repo.get_analytics_by_employee_all_time()
            # treat this as “all time” window
            return [
                AnalyticsResponse(
                    employee_id=row.employee_id,
                    employee_name=row.employee_name,
                    total_shifts=row.total_shifts,
                    total_hours=float(row.total_hours or 0),
                    period="all",
                    start_date=date.min,
                    end_date=date.max,
                )
                for row in rows
            ]
        start_date, end_date = self._get_period_range(period, ref_date)
        rows = self.shift_repo.get_analytics_by_employee(start_date, end_date)
        return [
            AnalyticsResponse(
                employee_id=row.employee_id,
                employee_name=getattr(row, "employee_name", None),
                total_shifts=row.total_shifts,
                total_hours=float(row.total_hours or 0),
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            for row in rows
        ]
