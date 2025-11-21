# backend/routes/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.response_models import OrderListItem, OrderResponse
from backend.models.request_models import UpdateStatusRequest
from backend.services.order_service import admin_list_orders, admin_update_status

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/orders", response_model=list[OrderListItem])
def list_orders(db: Session = Depends(get_db)):
    return admin_list_orders(db)


@router.post("/order/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: str, payload: UpdateStatusRequest, db: Session = Depends(get_db)):
    return admin_update_status(order_id, payload, db)
