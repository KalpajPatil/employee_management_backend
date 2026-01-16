from datetime import date, timedelta

from app.repositories.schedule import ShiftRepository
from app.schemas.analytics import AnalyticsResponse

class AnalyticsService:
    def __init__(self, shift_repo: ShiftRepository):
        self.shift_repo = shift_repo

    
    def _get_period_range(self, period: str, ref_date: date):
        if period == "day":
            return ref_date, ref_date

        if period == "week":
            # assuming Monday as first day
            start = ref_date - timedelta(days=ref_date.weekday())
            end = start + timedelta(days=6)
            return start, end

        if period == "month":
            start = ref_date.replace(day=1)
            if start.month == 12:
                next_month = start.replace(year=start.year + 1, month=1, day=1)
            else:
                next_month = start.replace(month=start.month + 1, day=1)
            end = next_month - timedelta(days=1)
            return start, end

        raise ValueError("Invalid period; use day, week, or month")

    def get_employee_analytics(self, period: str, ref_date: date):
        start_date, end_date = self._get_period_range(period, ref_date)
        rows = self.shift_repo.get_analytics_by_employee(start_date, end_date)
        return [
            AnalyticsResponse(
                employee_id=row.employee_id,
                total_shifts=row.total_shifts,
                total_hours=float(row.total_hours or 0),
            )
            for row in rows
        ]
