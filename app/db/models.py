# app/db/models.py
from sqlalchemy import Column, DateTime, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum
from app.db.base import Base
from app.db.enums import ShiftType

class EmployeeDB(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    availability = Column(Text, nullable=True) #optional so nullable=true

    shifts = relationship(
        "ShiftDB",
        back_populates="employee",
        cascade="all, delete-orphan",
    )


class ShiftDB(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    shift_date = Column(Date, nullable=False, index=True)
    shift = Column(
        SAEnum(ShiftType, name="shift_type_enum"),
        nullable=False,
    )
    note = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    employee = relationship("EmployeeDB", back_populates="shifts")

