from datetime import date, datetime
import logging
from typing import List, Optional
from app.core import exceptions
from sqlalchemy.orm import Session

from app.db.models import ShiftDB, EmployeeDB
from app.repositories.schedule import ShiftRepository
from app.repositories.employees import EmployeeRepository
from app.schemas.schedule import (
    ShiftCreate,
    ShiftUpdate,
    ShiftResponse,
)

logger = logging.getLogger(__name__)

class ShiftService:
    def __init__(self, db_session: Session) -> None:
        self.db_session: Session = db_session
        self.shift_repository: ShiftRepository = ShiftRepository(
            db=db_session
        )
        self.employee_repository = EmployeeRepository(
            db=db_session
        )

    def list_shifts(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        employee_id: Optional[int] = None,
        start_datetime_from: Optional[datetime] = None,
        start_datetime_to: Optional[datetime] = None,
        end_datetime_from: Optional[datetime] = None,
        end_datetime_to: Optional[datetime] = None,
    ) -> List[ShiftResponse]:
        shift_db_list: List[ShiftDB] = self.shift_repository.find_all(
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id,
            start_datetime_from=start_datetime_from,
            start_datetime_to=start_datetime_to,
            end_datetime_from=end_datetime_from,
            end_datetime_to=end_datetime_to,
        )

        shift_response_list: List[ShiftResponse] = [
            ShiftResponse.model_validate(shift_db)
            for shift_db in shift_db_list
        ]
        return shift_response_list

    def get_shift(self, shift_id: int) -> Optional[ShiftResponse]:
        shift_db: Optional[ShiftDB] = self.shift_repository.find_by_id(
            shift_id=shift_id
        )
        if shift_db is None:
            return None

        shift_response: ShiftResponse = ShiftResponse.model_validate(shift_db)
        return shift_response

    def create_shift(self, shift_in: ShiftCreate) -> ShiftResponse:
        
        self.validate_shift_times(start_time=shift_in.start_time, end_time=shift_in.end_time)

        employee: Optional[EmployeeDB] = self.employee_repository.find_by_id(
                employee_id=shift_in.employee_id
            )
         
        if employee is None:
            raise exceptions.EmployeeNotFoundError(employee_id=shift_in.employee_id)
        
        overlapping_shifts = self.shift_repository.find_overlapping_shifts_for_employee(
            employee_id=shift_in.employee_id,
            date_value=shift_in.shift_date,
            start_time=shift_in.start_time,
            end_time=shift_in.end_time,
        )

        if len(overlapping_shifts) > 0:
            raise exceptions.ShiftConflictError(
                message=(
                    "Employee already has a shift that overlaps with the requested "
                    "time window on this date"
                )
            )

        shift_db: ShiftDB = ShiftDB(
            employee_id=shift_in.employee_id,
            shift_date=shift_in.shift_date,
            shift=shift_in.shift,
            note=shift_in.note,
            start_time=shift_in.start_time,
            end_time=shift_in.end_time,
        )

        saved_shift_db: ShiftDB = self.shift_repository.save(shift=shift_db)

        shift_response: ShiftResponse = ShiftResponse.model_validate(
            saved_shift_db
        )
        return shift_response

    def update_shift(
        self,
        shift_id: int,
        shift_in: ShiftUpdate,
    ) -> Optional[ShiftResponse]:

        overlapping_shifts = self.shift_repository.find_overlapping_shifts_for_employee(
            employee_id=shift_in.employee_id,
            date_value=shift_in.shift_date,
            start_time=shift_in.start_time,
            end_time=shift_in.end_time,
            exclude_shift_id=shift_id
        )

        if len(overlapping_shifts) > 0:
            raise exceptions.ShiftConflictError(
                message=(
                    "Employee already has a shift that overlaps with the requested "
                    "time window on this date"
                )
            )
        
        existing_shift_db: Optional[ShiftDB] = self.shift_repository.find_by_id(
            shift_id=shift_id
        )
        if existing_shift_db is None:
            return None

        if shift_in.employee_id is not None:
            existing_shift_db.employee_id = shift_in.employee_id

        if ShiftDB.shift_date is not None:
            existing_shift_db.date = ShiftDB.shift_date

        if shift_in.shift is not None:
            existing_shift_db.shift = shift_in.shift

        if shift_in.note is not None:
            existing_shift_db.note = shift_in.note

        if shift_in.start_time is not None:
            existing_shift_db.start_time = shift_in.start_time

        if shift_in.end_time is not None:
            existing_shift_db.end_time = shift_in.end_time

        updated_shift_db: ShiftDB = self.shift_repository.save(
            shift=existing_shift_db
        )

        shift_response: ShiftResponse = ShiftResponse.model_validate(
            updated_shift_db
        )
        return shift_response

    def delete_shift(self, shift_id: int) -> bool:
        existing_shift_db: Optional[ShiftDB] = self.shift_repository.find_by_id(
            shift_id=shift_id
        )
        if existing_shift_db is None:
            return False

        self.shift_repository.delete(shift=existing_shift_db)
        return True

    def validate_shift_times(self, start_time, end_time) -> None:
        """
        Validate that a shift's end_time is after start_time.
        Raise ValueError if invalid.
        """
        if end_time is None or start_time is None:
            raise exceptions.ShiftConflictError("start_time and end_time are required")

        if end_time <= start_time:
            raise exceptions.ShiftConflictError("end_time must be strictly after start_time")