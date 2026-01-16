# app/core/config.py
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wasty.db")
ENV = os.getenv("ENV", "dev")
