from pytest_bdd import scenario
from tests.steps.test_checkout_feature_real_app import *


@scenario(
    "features/test_checkout_feature_real_app.feature",
    "Group of 4 people orders full meal and gets correct total before 19",
)
def test_group_of_4_before_19():
    pass


@scenario(
    "features/test_checkout_feature_real_app.feature",
    "Group of 4 people orders full meal and gets correct total",
)
def test_group_of_4():
    pass


@scenario(
    "features/test_checkout_feature_real_app.feature",
    "Two people order before 19:00, two more join after 20:00",
)
def test_two_people_join_later():
    pass


@scenario(
    "features/test_checkout_feature_real_app.feature", "A member cancel its order"
)
def test_cancel_order():
    pass
