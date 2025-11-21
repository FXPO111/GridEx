# backend/routes/exchange.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.request_models import CreateOrderRequest
from backend.models.response_models import OrderResponse
from backend.services.order_service import create_order

router = APIRouter(prefix="/api/exchange", tags=["exchange"])


@router.post("/create", response_model=OrderResponse)
def create_exchange_order(payload: CreateOrderRequest, db: Session = Depends(get_db)):
    return create_order(payload, db)
