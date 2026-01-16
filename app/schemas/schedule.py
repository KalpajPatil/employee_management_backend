from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.db.enums import ShiftType


class ShiftBase(BaseModel):
    employee_id: int = Field(
        ...,
        description="Identifier of the employee assigned to this shift",
        example=1,
    )
    shift_date: date = Field(
        ...,
        description="Calendar date of the shift",
        example="2025-05-21",
    )
    shift: ShiftType = Field(
        ...,
        description="Type of shift",
        example=ShiftType.MORNING,
    )
    note: Optional[str] = Field(
        default=None,
        description="Optional note for the shift",
        example="Covering for Sam",
    )
    start_time: datetime = Field(
        ...,
        description="Start date and time of the shift",
        example="2025-05-21T09:00:00",
    )
    end_time: datetime = Field(
        ...,
        description="End date and time of the shift",
        example="2025-05-21T17:00:00",
    )


class ShiftCreate(ShiftBase):
    # Same fields as base, but separated for future changes
    pass


class ShiftUpdate(BaseModel):
    employee_id: Optional[int] = Field(
        default=None,
        description="New employee identifier for this shift",
        example=2,
    )
    shift_date: Optional[date] = Field(
        default=None,
        description="New date for the shift",
        example="2025-05-22",
    )
    shift: Optional[ShiftType] = Field(
        default=None,
        description="New type of shift",
        example=ShiftType.AFTERNOON,
    )
    note: Optional[str] = Field(
        default=None,
        description="New note for the shift",
        example="Swapped with Chris",
    )
    start_time: Optional[datetime] = Field(
        default=None,
        description="New start date and time of the shift",
        example="2025-05-22T10:00:00",
    )
    end_time: Optional[datetime] = Field(
        default=None,
        description="New end date and time of the shift",
        example="2025-05-22T18:00:00",
    )


class ShiftResponse(ShiftBase):
    id: int = Field(
        ...,
        description="Unique identifier of the shift",
        example=101,
    )

    class Config:
        from_attributes = True
