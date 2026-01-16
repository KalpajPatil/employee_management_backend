class EmployeeNotFoundError(Exception):
    def __init__(self, employee_id: int) -> None:
        self.employee_id = employee_id
        self.message = f"Employee with id={employee_id} does not exist"
        super().__init__(self.message)


class ShiftConflictError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
