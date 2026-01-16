# app/repositories/employees.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.models import EmployeeDB


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    # find all employees
    def find_all(self) -> List[EmployeeDB]:
        return self.db.query(EmployeeDB).all()

    # find employee by id
    def find_by_id(self, employee_id: int) -> Optional[EmployeeDB]:
        return (
            self.db.query(EmployeeDB)
            .filter(EmployeeDB.id == employee_id)
            .first()
        )

    # save a newly created employee
    def save(self, employee: EmployeeDB) -> EmployeeDB:
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    # delete an employee record from the table
    def delete(self, employee: EmployeeDB) -> None:
        self.db.delete(employee)
        self.db.commit()
