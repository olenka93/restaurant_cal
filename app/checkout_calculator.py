from datetime import datetime
from typing import Dict, List, Optional

from config.config_loader import load_pricing_config
from models.order_model import ItemType, OrderItem


class CheckoutCalculator:
    TIME_FORMAT = "%H:%M"

    def __init__(
        self, items_with_qty: List[Dict[str, any]], order_time: Optional[str] = None
    ):
        self.pricing_config = load_pricing_config()
        self.order_items = [
            OrderItem(
                item_type=ItemType(item["item"]),
                quantity=int(item["quantity"]),
                order_time=self._parse_order_time(order_time),
            )
            for item in items_with_qty
        ]

    def _parse_order_time(self, order_time: Optional[str]) -> Optional[datetime]:
        if not order_time:
            return None

        try:
            return datetime.strptime(order_time, self.TIME_FORMAT)
        except (ValueError, TypeError):
            raise ValueError("Invalid order time format. Must be HH:MM. Example: 18:30")

    def _is_early_bird_eligible(self, order_time: Optional[datetime]) -> bool:
        if not order_time:
            return False
        return order_time.time() < self.pricing_config.discount_cutoff_time

    def _calculate_item_price(self, order_item: OrderItem) -> float:
        base_price = self.pricing_config.item_prices[order_item.item_type]
        if order_item.item_type == ItemType.DRINK and self._is_early_bird_eligible(
            order_item.order_time
        ):
            base_price *= 1 - self.pricing_config.drink_discount_rate
        return base_price * order_item.quantity

    def calculate_total(self) -> float:
        """
        Calculates the total cost of an order including service charge based
        on the type of items (food or drink) in the order.

        The function computes the cost of food items and drink items
        separately. It then applies a service charge to the food total and
        combines all parts to determine the final order total.

        :return: The rounded total cost of the order including service charge.
        :rtype: float
        """
        food_total = sum(
            self._calculate_item_price(item)
            for item in self.order_items
            if item.is_food
        )
        drink_total = sum(
            self._calculate_item_price(item)
            for item in self.order_items
            if not item.is_food
        )

        service_charge = food_total * self.pricing_config.service_charge_rate
        total = food_total + service_charge + drink_total

        return round(total, 2)

    def cancel_items(self, items_to_cancel: List[Dict[str, any]]) -> None:
        """
        Cancel specific items from the order.

        Args:
            items_to_cancel: List of dictionaries containing item type and quantity to cancel
                           Format: [{"item": "starter", "quantity": 1}, ...]

        Raises:
            ValueError: If trying to cancel more items than ordered or invalid item type
        """
        # Convert items_to_cancel to a more manageable format
        cancellations = {
            ItemType(item["item"]): int(item["quantity"]) for item in items_to_cancel
        }

        # Create new order items list
        new_order_items = []

        for order_item in self.order_items:
            if order_item.item_type in cancellations:
                cancelled_qty = cancellations[order_item.item_type]
                if cancelled_qty > order_item.quantity:
                    raise ValueError(
                        f"Cannot cancel {cancelled_qty} of {order_item.item_type.value}, "
                        f"only {order_item.quantity} were ordered"
                    )
                remaining_qty = order_item.quantity - cancelled_qty
                if remaining_qty > 0:
                    order_item.quantity = remaining_qty
                    new_order_items.append(order_item)
            else:
                new_order_items.append(order_item)
        self.order_items = new_order_items

    def add_items(
        self, items: List[Dict[str, any]], order_time: Optional[str] = None
    ) -> None:
        """
        Add new items to the existing order with their own order time.

        Args:
            items: List of dictionaries containing item type and quantity to add
                  Format: [{"item": "starter", "quantity": 1}, ...]
            order_time: Time of the additional order (optional)

        Raises:
            ValueError: If an invalid item type is provided
        """
        parsed_time = self._parse_order_time(order_time)

        new_items = [
            OrderItem(
                item_type=ItemType(item["item"]),
                quantity=int(item["quantity"]),
                order_time=parsed_time,
            )
            for item in items
        ]

        self.order_items.extend(new_items)
