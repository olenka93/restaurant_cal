import logging
from tests.utils.test_utils import check_response
from pytest_bdd import given, parsers, then, when
import requests

BASE_URL = "http://localhost:5000"
logger = logging.getLogger("bdd-tests")


@given(parsers.parse("the order payload is:"))
def order_payload(context, datatable, parse_gherkin_table):
    context["items"] = parse_gherkin_table(datatable)
    logger.info(f"Prepared order payload with {len(context['items'])} items")


@given(parsers.parse('the order time is "{order_time}"'))
def set_order_time(context, order_time):
    context["order_time"] = order_time


@when("the order is submitted")
def submit_order(context):
    payload = {"items": context["items"]}
    if "order_time" in context:
        payload["order_time"] = context["order_time"]
    logger.info(f"Submitting order with payload: {payload}")
    response = requests.post(f"{BASE_URL}/order", json=payload)
    context["response"] = response
    check_response(response, "Order submission")
    context["order_id"] = response.json().get("order_id")
    logger.info(f"Submitted order, received order_id={context['order_id']}")


@when(parsers.parse('more items are added at "{order_time}":'))
@when(parsers.parse("more items are added:\n{table}"))
def add_more_items(context, datatable, parse_gherkin_table, order_time=None):
    formatted_items = parse_gherkin_table(datatable)

    payload = {"items": formatted_items}
    if order_time:
        payload["order_time"] = order_time

    response = requests.post(
        f"{BASE_URL}/orders/{context['order_id']}/add", json=payload
    )
    context["response"] = response
    check_response(response, "Add more items")


@when(parsers.parse("items are canceled:"))
def cancel_items(context, datatable, parse_gherkin_table):
    formatted_items = parse_gherkin_table(datatable)

    payload = {"items": formatted_items}

    response = requests.post(
        f"{BASE_URL}/orders/{context['order_id']}/cancel", json=payload
    )
    context["response"] = response
    check_response(response, "Cancel items")


@then(parsers.parse("the total should be {expected_total:g}"))
def check_total(context, expected_total):
    order_id = context["order_id"]
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    check_response(response, "Get order items")
    actual_total = response.json().get("total")
    assert round(actual_total, 2) == round(expected_total, 2)
