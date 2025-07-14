from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ItemType(Enum):
    STARTER = "starter"
    MAIN = "main"
    DRINK = "drink"


@dataclass
class OrderItem:
    item_type: ItemType
    quantity: int
    order_time: Optional[datetime]

    @property
    def is_food(self) -> bool:
        return self.item_type in (ItemType.STARTER, ItemType.MAIN)

    def to_dict(self):
        return {
            "item": self.item_type.value,
            "quantity": self.quantity,
            "order_time": (
                self.order_time.strftime("%H:%M") if self.order_time else None
            ),
        }
