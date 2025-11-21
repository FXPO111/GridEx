# backend/utils/generate_order_id.py
import random
import string


def generate_public_id(length: int = 8) -> str:
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return "GX" + suffix
