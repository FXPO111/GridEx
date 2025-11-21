# backend/services/time_utils.py
from datetime import datetime, timedelta
from backend.config import settings


def now_utc() -> datetime:
    return datetime.utcnow()


def compute_lock_until() -> datetime:
    return now_utc() + timedelta(minutes=settings.LOCK_MINUTES)
