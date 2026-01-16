from typing import Optional
from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    name: str = Field(
        ...,
        description="Full name of the employee",
        example="Alex Morgan",
    )
    role: str = Field(
        ...,
        description="Role or job title of the employee",
        example="Operator",
    )
    availability: Optional[str] = Field(
        default=None,
        description="Optional description of employee availability",
        example="Mon-Fri, 09:00-17:00",
    )


class EmployeeCreate(EmployeeBase):
    # No extra fields for now, but separated for future extension
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="New name of the employee",
        example="Alex Morgan",
    )
    role: Optional[str] = Field(
        default=None,
        description="New role or job title of the employee",
        example="Manager",
    )
    availability: Optional[str] = Field(
        default=None,
        description="New availability description",
        example="Mon-Thu, 10:00-18:00",
    )


class EmployeeResponse(EmployeeBase):
    id: int = Field(
        ...,
        description="Unique identifier of the employee",
        example=1,
    )

    class Config:
        # Tell Pydantic it may receive ORM objects (EmployeeDB) and map them
        from_attributes = True
