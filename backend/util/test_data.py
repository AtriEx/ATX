"""Test data for testing transactions"""

from datetime import datetime, timedelta
from uuid import uuid4 as generate_order_id

# pylint: disable=R0801 # test data


def buy_entry(data: dict) -> dict:
    """
    Creates a test buy order table entry and returns it
    """
    test_entry = {
        "userId": "d8a7ae82-1704-41bf-96a3-9347a5c022c8",
        "buy_or_sell": True,
        "stockId": data["stockId"],
        "price": data["price"],
        "quantity": data["quantity"],
        "time_posted": datetime.now().isoformat(),
        "orderId": str(generate_order_id()),
        "expirey": (
            datetime.now() + timedelta(hours=1)
        ).isoformat(),  # This is a test value; users will input an expiry date
        "has_been_processed": False,
    }
    return test_entry


# pylint: disable=R0801 # test data
def sell_entry(data: dict) -> dict:
    """
    Creates a test sell order table entry and returns it
    """
    test_entry = {
        "userId": "572a902e-de7a-4739-adfe-f4af32a3f18b",
        "buy_or_sell": False,
        "stockId": data["stockId"],
        "price": data["price"],
        "quantity": data["quantity"],
        "orderId": str(generate_order_id()),
        "time_posted": datetime.now().isoformat(),
        "expirey": (
            datetime.now() + timedelta(hours=1)
        ).isoformat(),  # This is a test value; users will input an expiry date
        "has_been_processed": False,
    }
    return test_entry
