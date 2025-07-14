import logging
import sys
import traceback
import uuid
from functools import wraps
from http import HTTPStatus
from typing import Dict, List, Tuple, Callable
from flask import Flask, jsonify, request, Response
from app.checkout_calculator import CheckoutCalculator
from tests.logger_config import setup_logging

setup_logging()
logger = logging.getLogger("flask-app")
app = Flask(__name__)


# Store active orders in memory (in production, this should be a proper database)
active_orders = {}


def validate_checkout_data(data: Dict) -> Tuple[List, str]:
    """Validate and extract checkout data from request"""
    if not isinstance(data, dict):
        raise ValueError("Invalid request format: JSON object expected")

    items = data.get("items")
    order_time = data.get("order_time", "")

    if not isinstance(items, list):
        raise ValueError("Items must be a list")

    return items, order_time


def validate_modification_data(data: Dict) -> Tuple[List, str]:
    """Validate and extract modification data from request"""
    if not isinstance(data, dict):
        raise ValueError("Invalid request format: JSON object expected")
    items = data.get("items")
    if items is None:
        raise ValueError("Missing required 'items' field")

    order_time = data.get("order_time", "")

    if not isinstance(items, list):
        raise ValueError("Items must be a list")

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each item must be an object")
        if "item" not in item or "quantity" not in item:
            raise ValueError("Each item must have 'item' and 'quantity' fields")

    return items, order_time


def create_success_response(data: Dict) -> Tuple[Dict, int]:
    """Create successful response with data"""
    return jsonify(data), HTTPStatus.OK


def handle_errors(func: Callable) -> Callable[..., Tuple[Response, int]]:
    """
    Decorator that handles errors and provides detailed error information.
    Captures root cause, stack trace, and error context.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Response, int]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Get the full exception info
            exc_type, exc_value, exc_traceback = sys.exc_info()

            # Build detailed error information
            error_details = {
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
            }

            if app.debug:
                # Add stack trace in debug mode
                error_details["stack_trace"] = traceback.format_exception(
                    exc_type, exc_value, exc_traceback
                )
                error_details["root_cause"] = {
                    "file": exc_traceback.tb_frame.f_code.co_filename,
                    "line": exc_traceback.tb_lineno,
                    "function": exc_traceback.tb_frame.f_code.co_name,
                }

            # Determine appropriate status code
            if isinstance(e, ValueError):
                status_code = HTTPStatus.BAD_REQUEST
            elif isinstance(e, KeyError) or isinstance(e, LookupError):
                status_code = HTTPStatus.NOT_FOUND
            else:
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR

            return jsonify({"status": "error", "error": error_details}), status_code

    return wrapper


@app.route("/order", methods=["POST"])
@handle_errors
def create_order() -> Tuple[Dict, int]:
    logger.info("Received new order creation request")

    data = request.get_json()
    if data is None:
        logger.error("Invalid JSON in request body")
        raise ValueError("Invalid JSON in request body")
    items, order_time = validate_checkout_data(data)

    # Create new calculator instance
    calculator = CheckoutCalculator(items, order_time)

    # Generate order ID (in production, use proper ID generation)
    order_id = str(uuid.uuid4())
    active_orders[order_id] = calculator
    total = calculator.calculate_total()
    logger.info(f"Created order {order_id} with {len(items)} items. Total: {total}")

    return create_success_response(
        {
            "order_id": order_id,
            "total": total,
            "items": [item.to_dict() for item in calculator.order_items],
        }
    )


@app.route("/orders/<order_id>/add", methods=["POST"])
@handle_errors
def add_items(order_id: str) -> Tuple[Dict, int]:
    """Add items to the existing order"""
    if order_id not in active_orders:
        raise ValueError("Order not found", HTTPStatus.NOT_FOUND)

    data = request.get_json()
    if data is None:
        raise ValueError("Invalid JSON in request body")
    items, order_time = validate_modification_data(data)

    calculator = active_orders[order_id]
    calculator.add_items(items, order_time)
    logger.info(f"Added items {items} to order {order_id}")

    return create_success_response(
        {
            "order_id": order_id,
            "total": calculator.calculate_total(),
            "items": [item.to_dict() for item in calculator.order_items],
        }
    )


@app.route("/orders/<order_id>/cancel", methods=["POST"])
@handle_errors
def cancel_items(order_id: str) -> Tuple[Dict, int]:
    """Add items to the existing order"""
    if order_id not in active_orders:
        raise ValueError("Order not found", HTTPStatus.NOT_FOUND)

    data = request.get_json()
    if data is None:
        raise ValueError("Invalid JSON in request body")
    items, _ = validate_modification_data(data)

    calculator = active_orders[order_id]
    calculator.cancel_items(items)
    logger.info(f"Canceled items {items} from order {order_id}")

    return create_success_response(
        {
            "order_id": order_id,
            "total": calculator.calculate_total(),
            "items": [item.to_dict() for item in calculator.order_items],
        }
    )


@app.route("/orders/<order_id>", methods=["GET"])
@handle_errors
def get_order_total(order_id: str) -> Tuple[Dict, int]:
    """Add items to the existing order"""
    if order_id not in active_orders:
        raise ValueError("Order not found", HTTPStatus.NOT_FOUND)

    calculator = active_orders[order_id]
    return create_success_response(
        {
            "order_id": order_id,
            "total": calculator.calculate_total(),
            "items": [item.to_dict() for item in calculator.order_items],
        }
    )


if __name__ == "__main__":
    app.run(debug=False)
