from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.schedule import (
    ShiftCreate,
    ShiftUpdate,
    ShiftResponse,
)
from app.services.schedule import ShiftService


router = APIRouter()


def get_shift_service(db: Session = Depends(get_db)) -> ShiftService:
    shift_service: ShiftService = ShiftService(db_session=db)
    return shift_service


@router.get(
    "",
    response_model=List[ShiftResponse],
    status_code=status.HTTP_200_OK,
)
def list_shifts(
    start_date: Optional[date] = Query(
        default=None,
        description="Filter by start date (inclusive)",
    ),
    end_date: Optional[date] = Query(
        default=None,
        description="Filter by end date (inclusive)",
    ),
    employee_id: Optional[int] = Query(
        default=None,
        description="Filter by employee id",
    ),
    start_datetime_from: Optional[datetime] = Query(
        default=None,
        description="Filter shifts with start_time >= this value",
    ),
    start_datetime_to: Optional[datetime] = Query(
        default=None,
        description="Filter shifts with start_time <= this value",
    ),
    end_datetime_from: Optional[datetime] = Query(
        default=None,
        description="Filter shifts with end_time >= this value",
    ),
    end_datetime_to: Optional[datetime] = Query(
        default=None,
        description="Filter shifts with end_time <= this value",
    ),
    shift_service: ShiftService = Depends(get_shift_service),
) -> List[ShiftResponse]:
    shifts: List[ShiftResponse] = shift_service.list_shifts(
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id,
        start_datetime_from=start_datetime_from,
        start_datetime_to=start_datetime_to,
        end_datetime_from=end_datetime_from,
        end_datetime_to=end_datetime_to,
    )
    return shifts


@router.get(
    "/{shift_id}",
    response_model=ShiftResponse,
    status_code=status.HTTP_200_OK,
)
def get_shift(
    shift_id: int,
    shift_service: ShiftService = Depends(get_shift_service),
) -> ShiftResponse:
    shift = shift_service.get_shift(shift_id=shift_id)
    if shift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )
    return shift


@router.post(
    "",
    response_model=ShiftResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shift(
    shift_in: ShiftCreate,
    shift_service: ShiftService = Depends(get_shift_service),
) -> ShiftResponse:
    created_shift: ShiftResponse = shift_service.create_shift(
        shift_in=shift_in
    )
    return created_shift


@router.put(
    "/{shift_id}",
    response_model=ShiftResponse,
    status_code=status.HTTP_200_OK,
)
def update_shift(
    shift_id: int,
    shift_in: ShiftUpdate,
    shift_service: ShiftService = Depends(get_shift_service),
) -> ShiftResponse:
    updated_shift = shift_service.update_shift(
        shift_id=shift_id,
        shift_in=shift_in,
    )
    if updated_shift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )
    return updated_shift


@router.delete(
    "/{shift_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_shift(
    shift_id: int,
    shift_service: ShiftService = Depends(get_shift_service),
) -> None:
    deleted: bool = shift_service.delete_shift(shift_id=shift_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )
    return None
