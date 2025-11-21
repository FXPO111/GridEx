# backend/services/order_service.py
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.db_models import Order
from backend.models.request_models import CreateOrderRequest, UpdateStatusRequest
from backend.utils.generate_order_id import generate_public_id
from backend.services.time_utils import compute_lock_until, now_utc
from backend.services.rates import get_effective_rate, calc_usdt_net
from backend.models.response_models import OrderResponse, OrderListItem
from fastapi import HTTPException


def create_order(payload: CreateOrderRequest, db: Session) -> OrderResponse:
    if payload.rub_amount < 1000:
        raise HTTPException(status_code=400, detail="Минимальная сумма 1000 RUB")

    if not payload.wallet.startswith("T"):
        raise HTTPException(status_code=400, detail="Некорректный TRC20 кошелёк")

    rate = get_effective_rate()
    usdt_net, _ = calc_usdt_net(payload.rub_amount, rate)

    public_id = generate_public_id()
    lock_until = compute_lock_until()

    order = Order(
        public_id=public_id,
        direction=payload.direction,
        rub_amount=payload.rub_amount,
        usdt_amount=usdt_net,
        rate=rate,
        wallet=payload.wallet,
        status="pending_payment",
        lock_until=lock_until,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return OrderResponse(
        order_id=order.public_id,
        direction=order.direction,
        rub_amount=order.rub_amount,
        usdt_amount=order.usdt_amount,
        rate=order.rate,
        wallet=order.wallet,
        status=order.status,
        lock_until=order.lock_until,
        card_number=settings.CARD_NUMBER,
    )


def _get_order(db: Session, order_id: str) -> Order:
    order = db.query(Order).filter(Order.public_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return order


def get_order(order_id: str, db: Session) -> OrderResponse:
    order = _get_order(db, order_id)
    return OrderResponse(
        order_id=order.public_id,
        direction=order.direction,
        rub_amount=order.rub_amount,
        usdt_amount=order.usdt_amount,
        rate=order.rate,
        wallet=order.wallet,
        status=order.status,
        lock_until=order.lock_until,
        card_number=settings.CARD_NUMBER,
    )


def mark_paid(order_id: str, db: Session) -> OrderResponse:
    order = _get_order(db, order_id)

    if order.status not in ("pending_payment", "paid"):
        raise HTTPException(status_code=400, detail=f"Нельзя отметить оплаченной из статуса {order.status}")

    order.status = "paid"
    order.updated_at = now_utc()
    db.add(order)
    db.commit()
    db.refresh(order)

    return get_order(order_id, db)


def admin_list_orders(db: Session) -> list[OrderListItem]:
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return [
        OrderListItem(
            order_id=o.public_id,
            rub_amount=o.rub_amount,
            usdt_amount=o.usdt_amount,
            status=o.status,
            created_at=o.created_at,
        )
        for o in orders
    ]


def admin_update_status(order_id: str, payload: UpdateStatusRequest, db: Session) -> OrderResponse:
    allowed = {"confirmed", "completed", "canceled"}
    if payload.status not in allowed:
        raise HTTPException(status_code=400, detail=f"Недопустимый статус. Можно: {', '.join(allowed)}")

    order = _get_order(db, order_id)
    order.status = payload.status
    order.updated_at = now_utc()
    db.add(order)
    db.commit()
    db.refresh(order)

    return get_order(order_id, db)
