"""Test data for testing transactions"""

from datetime import datetime, timedelta
from uuid import uuid4 as generate_order_id

# pylint: disable=R0801 # test data


def test_entry_1() -> dict:
    """
    Creates a test buy order table entry and returns it
    """
    test_entry = {
        "userId": "d8a7ae82-1704-41bf-96a3-9347a5c022c8",
        "buy_or_sell": True,
        "stockId": 2,
        "price": 26,
        "quantity": 11,
        "time_posted": datetime.now().isoformat(),
        "orderId": str(generate_order_id()),
        "expirey": (
            datetime.now() + timedelta(hours=1)
        ).isoformat(),  # This is a test value; users will input an expiry date
    }
    return test_entry


# pylint: disable=R0801 # test data
def test_entry_2() -> dict:
    """
    Creates a test sell order table entry and returns it
    """
    test_entry = {
        "userId": "572a902e-de7a-4739-adfe-f4af32a3f18b",
        "buy_or_sell": False,
        "stockId": 2,
        "price": 25,
        "quantity": 1,
        "orderId": str(generate_order_id()),
        "time_posted": datetime.now().isoformat(),
        "expirey": (
            datetime.now() + timedelta(hours=1)
        ).isoformat(),  # This is a test value; users will input an expiry date
    }
    return test_entry
