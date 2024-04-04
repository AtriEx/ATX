import json
from tarfile import data_filter
from fastapi.testclient import TestClient

from main import app
from util import test_data
from database import supabase_middleman

client = TestClient(app)


def test_create_buy_order():
    data = {"stockId": 1, "price": 20, "quantity": 1}
    buy_data = test_data.buy_entry(data=data)
    # Check if market_open check works
    # Check if buy order receives proper data
    # Check if order can be fulfilled

    # Match Price Buyer Side
    match_price_buyer_side(data)

    # Match Price Seller Side
    match_price_seller_side(data)

    # Match Price Equidistant

    match_price_equidistant(data)

    # Buy Price Match

    buy_sell_price_match(data)


def buying_process(buy_data: dict, sell_data: dict, qb_response: str):
    # This is the current process for setting up buying/selling orders
    # This process will probably change so I separated it into a function

    # Insert sell order BEFORE buy order to test return statement
    response = client.post("/insertCustomOrder/", json=sell_data)
    assert response.status_code == 200
    assert response.json == "Custom Order inserted"

    response = client.post("/insertCustomOrder/", json=buy_data)
    assert response.status_code == 200
    assert response == "Custom Order inserted"

    ids = supabase_middleman.fetch_id_from_order_id(buy_data["order_id"])
    for id in ids:
        buy_data["Id"] = id
        response = client.post("/qb/", json=buy_data)
        assert response.status_code == 200
        assert response == qb_response


def match_price_buyer_side(data):
    current_price = supabase_middleman.fetch_stock_price(1)
    assert current_price > 5

    data["price"] = current_price + 4
    buy_data = test_data.buy_entry(data=data)

    # Seller price should be further from market price than buyer price
    data["price"] = current_price - 5
    sell_data = test_data.sell_entry(data=data)

    response = buying_process(
        buy_data, sell_data, "Order fulfilled at buyers price. No refund needed."
    )


def match_price_seller_side(data):
    current_price = supabase_middleman.fetch_stock_price(1)
    assert current_price > 5

    data["price"] = current_price + 4
    sell_data = test_data.sell_entry(data=data)

    # Buyer price should be further from market price than seller price
    data["price"] = current_price - 5
    buy_data = test_data.buy_entry(data=data)

    response = buying_process(
        buy_data, sell_data, "Order fulfilled at sellers price. refund issued to buyer"
    )


def buy_sell_price_match(data):
    current_price = supabase_middleman.fetch_stock_price(1)
    # buy price = sell price != current market price
    data["price"] = current_price + 5
    # Orders should match price not at the market price
    buy_data = test_data.buy_entry(data=data)
    sell_data = test_data.sell_entry(data=data)
    response = buying_process(buy_data, sell_data, "Order fulfilled at desired price")


def match_price_equidistant(data):
    current_price = supabase_middleman.fetch_stock_price(1)
    assert current_price > 5

    data["price"] = current_price + 5
    sell_data = test_data.sell_entry(data=data)

    # Both prices are the same distance from market price
    data["price"] = current_price - 5
    buy_data = test_data.buy_entry(data=data)

    response = buying_process(
        buy_data, sell_data, "Order fulfilled at current price. Refund issued to buyer."
    )
