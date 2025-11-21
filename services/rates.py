# backend/services/rates.py
import random
from backend.config import settings


def get_effective_rate() -> float:
    """
    Берём базовый курс и добавляем легкий джиттер ±0.5%.
    """
    base = settings.BASE_RATE
    jitter = (random.random() - 0.5) * 0.01  # ±0.5%
    return base * (1 + jitter)


def calc_usdt_net(rub_amount: float, rate: float) -> tuple[float, float]:
    """
    Возвращает (net_usdt, fee_usdt)
    """
    gross = rub_amount * rate
    fee = gross * settings.FEE_PCT
    net = gross - fee
    return net, fee
