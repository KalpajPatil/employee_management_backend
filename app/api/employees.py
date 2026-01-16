from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.employees import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
)
from app.services.employees import EmployeeService


router = APIRouter()


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    employee_service: EmployeeService = EmployeeService(db_session=db)
    return employee_service


@router.get(
    "",
    response_model=List[EmployeeResponse],
    status_code=status.HTTP_200_OK,
)
def list_employees(
    employee_service: EmployeeService = Depends(get_employee_service),
) -> List[EmployeeResponse]:
    employees: List[EmployeeResponse] = employee_service.list_employees()
    return employees


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
)
def get_employee(
    employee_id: int,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    employee = employee_service.get_employee(employee_id=employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee_in: EmployeeCreate,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    created_employee: EmployeeResponse = employee_service.create_employee(
        employee_in=employee_in
    )
    return created_employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
)
def update_employee(
    employee_id: int,
    employee_in: EmployeeUpdate,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    updated_employee = employee_service.update_employee(
        employee_id=employee_id,
        employee_in=employee_in,
    )
    if updated_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return updated_employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_employee(
    employee_id: int,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> None:
    deleted: bool = employee_service.delete_employee(employee_id=employee_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return None
