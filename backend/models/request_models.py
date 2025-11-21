# backend/models/request_models.py
from pydantic import BaseModel, Field


class CreateOrderRequest(BaseModel):
    direction: str = Field(example="rub-card-to-usdt-trc20")
    rub_amount: float = Field(gt=0, example=10000)
    wallet: str = Field(min_length=10, example="TXXXX...TRON")


class UpdateStatusRequest(BaseModel):
    status: str = Field(example="confirmed")  # confirmed / completed / canceled
