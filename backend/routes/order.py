# backend/routes/order.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.response_models import OrderResponse
from backend.services.order_service import get_order, mark_paid

router = APIRouter(prefix="/api/order", tags=["order"])


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_endpoint(order_id: str, db: Session = Depends(get_db)):
    return get_order(order_id, db)


@router.post("/{order_id}/paid", response_model=OrderResponse)
def mark_paid_endpoint(order_id: str, db: Session = Depends(get_db)):
    return mark_paid(order_id, db)
