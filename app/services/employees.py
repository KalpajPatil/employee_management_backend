from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.models import EmployeeDB
from app.repositories.employees import EmployeeRepository
from app.schemas.employees import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
)


class EmployeeService:
    def __init__(self, db_session: Session) -> None:
        self.db_session: Session = db_session
        self.employee_repository: EmployeeRepository = EmployeeRepository(
            db=db_session
        )

    def list_employees(self) -> List[EmployeeResponse]:
        employee_db_list: List[EmployeeDB] = self.employee_repository.find_all()
        employee_response_list: List[EmployeeResponse] = [
            EmployeeResponse.model_validate(employee_db)
            for employee_db in employee_db_list
        ]
        return employee_response_list

    def get_employee(self, employee_id: int) -> Optional[EmployeeResponse]:
        employee_db: Optional[EmployeeDB] = self.employee_repository.find_by_id(
            employee_id=employee_id
        )
        if employee_db is None:
            return None

        employee_response: EmployeeResponse = EmployeeResponse.model_validate(
            employee_db
        )
        return employee_response

    def create_employee(self, employee_in: EmployeeCreate) -> EmployeeResponse:
        employee_db: EmployeeDB = EmployeeDB(
            name=employee_in.name,
            role=employee_in.role,
            availability=employee_in.availability,
        )

        saved_employee_db: EmployeeDB = self.employee_repository.save(
            employee=employee_db
        )

        employee_response: EmployeeResponse = EmployeeResponse.model_validate(
            saved_employee_db
        )
        return employee_response

    def update_employee(
        self,
        employee_id: int,
        employee_in: EmployeeUpdate,
    ) -> Optional[EmployeeResponse]:
        existing_employee_db: Optional[EmployeeDB] = (
            self.employee_repository.find_by_id(employee_id=employee_id)
        )
        if existing_employee_db is None:
            return None

        if employee_in.name is not None:
            existing_employee_db.name = employee_in.name

        if employee_in.role is not None:
            existing_employee_db.role = employee_in.role

        if employee_in.availability is not None:
            existing_employee_db.availability = employee_in.availability

        updated_employee_db: EmployeeDB = self.employee_repository.save(
            employee=existing_employee_db
        )

        employee_response: EmployeeResponse = EmployeeResponse.model_validate(
            updated_employee_db
        )
        return employee_response

    def delete_employee(self, employee_id: int) -> bool:
        existing_employee_db: Optional[EmployeeDB] = (
            self.employee_repository.find_by_id(employee_id=employee_id)
        )
        if existing_employee_db is None:
            return False

        self.employee_repository.delete(employee=existing_employee_db)
        return True
