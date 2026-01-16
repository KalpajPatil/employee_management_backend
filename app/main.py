import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from app.core.exception_handlers import employee_not_found_handler, general_exception_handler, http_exception_handler, shift_conflict_handler
from app.core.exceptions import EmployeeNotFoundError, ShiftConflictError
from app.db.base import Base, engine
from app.api import analytics, employees, schedule

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE_PATH = LOG_DIR / "wasty_backend.log"

log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

file_handler = RotatingFileHandler(
    filename=LOG_FILE_PATH,
    maxBytes=5 * 1024 * 1024,   # 5 MB per file
    backupCount=3,              # keep 3 old files
)

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format))

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger("wasty_app")
logger.info("Logging configured: file=%s", LOG_FILE_PATH)

sql_logger = logging.getLogger("sqlalchemy.engine")
sql_logger.setLevel(logging.INFO)


# Create DB tables for all models registered on Base
Base.metadata.create_all(bind=engine)

# Main FastAPI application object
app = FastAPI(title="Wasty Employee Scheduling API")


# Register routers (controllers) with the app
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
# Register exception handlers
app.add_exception_handler(EmployeeNotFoundError, employee_not_found_handler)
app.add_exception_handler(ShiftConflictError, shift_conflict_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
