import logging
from pytest_bdd import when, then, parsers, given
import responses
import requests
from http import HTTPStatus

logger = logging.getLogger("bdd-tests")
BASE_URL = "http://localhost:5000"


@when("the order submission fails with server error")
def submit_order_with_error(mock_responses, context):
    mock_responses.add(
        responses.POST,
        f"{BASE_URL}/order",
        json={"error": "Internal Server Error"},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    payload = {"items": context["items"]}
    if "order_time" in context:
        payload["order_time"] = context["order_time"]

    response = requests.post(f"{BASE_URL}/order", json=payload)
    context["response"] = response
    logger.info(f"Submitted order, received response: {response.text}")
    return response


@then(parsers.parse("the response status code should be {status_code:d}"))
def check_status_code(context, status_code):
    assert context["response"].status_code == status_code


@then("the response should contain an error message")
def check_error_message(context):
    response_data = context["response"].json()
    assert "error" in response_data
    assert response_data["error"] == "Internal Server Error"


@given("an order payload with non-list items")
def non_list_items_payload(context):
    context["payload"] = {"items": "this should be a list but it's a string"}


@when("the order invalid is submitted")
def submit_invalid_order(context):
    response = requests.post(f"{BASE_URL}/order", json=context["payload"])
    context["response"] = response
    logger.info(f"Submitted invalid order, received response: {response.status_code}")


@then(parsers.parse('the error message should mention "{expected_message}"'))
def check_error_message(context, expected_message):
    response_data = context["response"].json()
    assert "error" in response_data
    assert "error_message" in response_data["error"]
    assert expected_message in response_data["error"]["error_message"]
