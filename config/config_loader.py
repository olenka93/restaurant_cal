import os

import yaml
from datetime import datetime
from config.checkout_config import PricingConfig
from models.order_model import ItemType


def load_pricing_config(path: str = None) -> PricingConfig:
    if path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "params.yaml")
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    required_fields = [
        "item_prices",
        "service_charge_rate",
        "drink_discount_rate",
        "discount_cutoff_time",
    ]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields in config: {missing_fields}")
    valid_items = {item.name for item in ItemType}
    invalid_items = set(data["item_prices"].keys()) - valid_items
    if invalid_items:
        raise ValueError(f"Invalid item types in config: {invalid_items}")

    item_prices = {
        ItemType[item]: float(price) for item, price in data["item_prices"].items()
    }
    try:
        service_charge_rate = float(data["service_charge_rate"])
        drink_discount_rate = float(data["drink_discount_rate"])
        if not (0 <= service_charge_rate <= 1 and 0 <= drink_discount_rate <= 1):
            raise ValueError("Rates must be between 0 and 1")
    except ValueError:
        raise ValueError("Invalid numeric values in configuration")

    return PricingConfig(
        item_prices=item_prices,
        service_charge_rate=service_charge_rate,
        drink_discount_rate=drink_discount_rate,
        discount_cutoff_time=datetime.strptime(
            data["discount_cutoff_time"], "%H:%M"
        ).time(),
    )
