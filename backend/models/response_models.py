from datetime import datetime
from pydantic import BaseModel


class OrderResponse(BaseModel):
    order_id: str
    direction: str
    rub_amount: float
    usdt_amount: float
    rate: float
    wallet: str
    status: str
    lock_until: datetime

    card_number: str | None = None

    class Config:
        orm_mode = True


class OrderListItem(BaseModel):
    order_id: str
    rub_amount: float
    usdt_amount: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
