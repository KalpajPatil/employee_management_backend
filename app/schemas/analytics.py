from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date


class AnalyticsBase(BaseModel):
    employee_id: int = Field(
        ...,
        description="Unique identifier of the employee",
        example=1,
    )
    employee_name: Optional[str] = Field(
        default=None,
        description="Name of the employee (optional, if joined in query)",
        example="Alex Morgan",
    )
    total_shifts: int = Field(
        ...,
        description="Total number of shifts in the selected period",
        example=10,
    )
    total_hours: float = Field(
        ...,
        description="Total hours worked in the selected period",
        example=82.5,
    )


class AnalyticsResponse(AnalyticsBase):
    period: str = Field(
        ...,
        description="Aggregation period: day, week, or month",
        example="week",
    )
    start_date: date = Field(
        ...,
        description="Start date of the aggregation window (inclusive)",
        example="2026-01-01",
    )
    end_date: date = Field(
        ...,
        description="End date of the aggregation window (inclusive)",
        example="2026-01-07",
    )

    class Config:
        from_attributes = True
