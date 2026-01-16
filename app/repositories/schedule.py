from datetime import date, datetime
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import EmployeeDB, ShiftDB

logger = logging.getLogger(__name__)
class ShiftRepository:
    def __init__(self, db: Session) -> None:
        # Store the session instance on the repository
        self.db: Session = db

    def find_all(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        employee_id: Optional[int] = None,
        start_datetime_from: Optional[datetime] = None,
        start_datetime_to: Optional[datetime] = None,
        end_datetime_from: Optional[datetime] = None,
        end_datetime_to: Optional[datetime] = None,
    ) -> List[ShiftDB]:
        # Start with a base query selecting from ShiftDB
        database_session: Session = self.db
        query_for_shifts = database_session.query(ShiftDB)

        # If a start_date filter was provided, apply it
        if start_date is not None:
            query_for_shifts = query_for_shifts.filter(
                ShiftDB.shift_date >= start_date
            )

        # If an end_date filter was provided, apply it
        if end_date is not None:
            query_for_shifts = query_for_shifts.filter(
                ShiftDB.shift_date <= end_date
            )

        # If an employee_id filter was provided, apply it
        if employee_id is not None:
            query_for_shifts = query_for_shifts.filter(
                ShiftDB.employee_id == employee_id
            )

        # Filter shifts whose start_time is >= a given datetime
        if start_datetime_from is not None:
            query_for_shifts = query_for_shifts.filter(
                ShiftDB.start_time >= start_datetime_from
            )

        # Filter shifts whose start_time is <= a given datetime
        if start_datetime_to is not None:
            query_for_shifts = query_for_shifts.filter(
                ShiftDB.start_time <= start_datetime_to
            )

        # Filter shifts whose end_time is >= a given datetime
        if end_datetime_from is not None:
            query_for_shifts = query_for_shifts.filter(
                ShiftDB.end_time >= end_datetime_from
            )

        # Filter shifts whose end_time is <= a given datetime
        if end_datetime_to is not None:
            query_for_shifts = query_for_shifts.filter(
                ShiftDB.end_time <= end_datetime_to
            )

        # Order the results by date in ascending order
        ordered_query_for_shifts = query_for_shifts.order_by(
            ShiftDB.shift_date.asc()
        )

        # Execute the query and get all results as a list
        list_of_shifts: List[ShiftDB] = ordered_query_for_shifts.all()

        return list_of_shifts

    def find_by_id(self, shift_id: int) -> Optional[ShiftDB]:
        # Get the current session
        database_session: Session = self.db

        # Build a query that filters by the primary key id
        query_for_single_shift = database_session.query(ShiftDB).filter(
            ShiftDB.id == shift_id
        )

        # Get the first matching result or None
        shift: Optional[ShiftDB] = query_for_single_shift.first()

        return shift

    def save(self, shift: ShiftDB) -> ShiftDB:
        # Get the current session
        database_session: Session = self.db

        # Add the shift instance to the session so it is tracked
        shift_instance: ShiftDB = shift
        database_session.add(shift_instance)

        # Commit the transaction so changes are written to the database
        database_session.commit()

        # Refresh the instance so any database-generated fields are loaded
        database_session.refresh(shift_instance)

        # Return the managed instance
        return shift_instance

    def delete(self, shift: ShiftDB) -> None:
        # Get the current session
        database_session: Session = self.db

        # Mark the given shift instance for deletion
        shift_instance: ShiftDB = shift
        database_session.delete(shift_instance)

        # Commit the transaction so the row is removed from the database
        database_session.commit()

    def find_overlapping_shifts_for_employee(
        self,
        employee_id: int,
        date_value: date, 
        start_time: datetime,
        end_time: datetime,
        exclude_shift_id: int | None = None,
    ) -> List[ShiftDB]:
        database_session: Session = self.db
        query_for_shifts = database_session.query(ShiftDB).filter(
            ShiftDB.employee_id == employee_id,
            ShiftDB.shift_date == date_value,
            ShiftDB.start_time < end_time,
            ShiftDB.end_time > start_time,
        )

        if exclude_shift_id is not None:
            query_for_shifts = query_for_shifts.filter(ShiftDB.id != exclude_shift_id)

        overlapping_shifts: List[ShiftDB] = query_for_shifts.all()
        return overlapping_shifts
    
    def get_analytics_by_employee_all_time(self):
        logger.info("inside get_analytics_by_employee_all_time")
        duration_hours = (
            (func.strftime('%s', ShiftDB.end_time) - func.strftime('%s', ShiftDB.start_time))
            / 3600.0
        )
        return (
            self.db.query(
                ShiftDB.employee_id.label("employee_id"),
                EmployeeDB.name.label("employee_name"),
                func.count(ShiftDB.id).label("total_shifts"),
                func.sum(duration_hours).label("total_hours"),
            )
            .join(EmployeeDB, EmployeeDB.id == ShiftDB.employee_id)
            .group_by(ShiftDB.employee_id, EmployeeDB.name)
            .all()
        )

    def get_analytics_by_employee(self, start_date, end_date):
        duration_hours = (
            (func.strftime('%s', ShiftDB.end_time) - func.strftime('%s', ShiftDB.start_time)) / 3600.0
        )
        session = self.db
        query = (
        session.query(
            ShiftDB.employee_id.label("employee_id"),
            EmployeeDB.name.label("employee_name"),
            func.count(ShiftDB.id).label("total_shifts"),
            func.sum(duration_hours).label("total_hours"),
        )
        .join(EmployeeDB, EmployeeDB.id == ShiftDB.employee_id)
        .filter(
            ShiftDB.shift_date >= start_date,
            ShiftDB.shift_date <= end_date,
        )
        .group_by(ShiftDB.employee_id, EmployeeDB.name)
    )
        return query.all()