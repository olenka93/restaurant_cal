from pytest_bdd import scenario
from tests.steps.test_order_errors_steps import *
from tests.steps.test_checkout_feature_real_app import *


@scenario(
    "features/test_order_errors.feature",
    "Order submission fails when items is not a list",
)
def test_order_submission_fails_when_items_is_not_a_list():
    pass
