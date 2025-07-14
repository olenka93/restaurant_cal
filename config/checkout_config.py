from dataclasses import dataclass
from typing import Dict
from datetime import time
from models.order_model import ItemType


@dataclass(frozen=True)
class PricingConfig:
    item_prices: Dict[ItemType, float]
    service_charge_rate: float
    drink_discount_rate: float
    discount_cutoff_time: time
