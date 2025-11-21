# backend/models/db_models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime

from backend.database.connection import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(16), unique=True, index=True, nullable=False)

    direction = Column(String(64), nullable=False)  # rub-card-to-usdt-trc20

    rub_amount = Column(Float, nullable=False)
    usdt_amount = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)

    wallet = Column(String(128), nullable=False)

    status = Column(String(32), nullable=False, default="pending_payment")
    lock_until = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
