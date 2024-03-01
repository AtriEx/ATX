"""API handler for creating and fulfilling buy orders."""

import os
from collections import deque
from util import test_data
from database import supabase_middleman
from dotenv import load_dotenv
# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root
from supabase import Client, create_client

load_dotenv("env/.env")

url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def buy_order():
    """Create a buy order for one share of a stock
    and fullfill it if possible."""
    # These are test values
    # We will have a function that returns this data using API call parameters
    buyer = test_data.test_entry_1()
    # Slects all active sells order by price then by time-posted (desc)
    valid_sells = (
        supabase.table("active_buy_sell")
        .select("Id", "userId", "time_posted", "buy_or_sell", "price",
                "quantity", "stockId", "orderId", "has_been_processed"
                )
        .match({"buy_or_sell": False, "stockId": buyer["stockId"]})
        .lte("price", buyer["price"])
        .order("price", desc=True)
        .order("time_posted")
        .limit(1)
        .execute()
        .data
    )
    # Market is open and a valid sell is availible
    if not valid_sells:
        # Insert the buy order into active_buy_sell if it can't be fufilled
        supabase_middleman.log_unfulfilled_order(buyer)
        print("No valid sells")

    # Gets sell order closest to the buy price
    seller = valid_sells.pop()
    # Finds the distances between the current price and the buy/sell prices
    # Decides order handling based off which price is closest to current price
    curr_price = supabase_middleman.fetch_stock_price(seller["stockId"])
    sell_diff = abs(curr_price - seller["price"])
    buy_diff = abs(buyer["price"] - curr_price)
    order_diff = buyer["price"] - seller["price"]
    # Checks edge case where buy price = sell price != current market price
    if order_diff == 0:
        # Order cannot be fulfilled @ current price
        supabase_middleman.sell_stock(seller["userId"], seller["stockId"], seller["price"])
        supabase_middleman.buy_stock(buyer["userId"], buyer["stockId"])
    elif sell_diff < buy_diff:
        # Order price=sell price; refund the difference between buy and sell price to the buyer
        supabase_middleman.sell_stock(seller["userId"], seller["stockId"], seller["price"])
        supabase_middleman.buy_stock(buyer["userId"], buyer["stockId"])
        supabase_middleman.resolve_price_diff(buyer["userId"], order_diff)
    elif buy_diff < sell_diff:
        # Order price = buy price; No refund needed because seller will sell @ higher price
        supabase_middleman.sell_stock(seller["userId"], seller["stockId"], buyer["price"])
        supabase_middleman.buy_stock(buyer["userId"], buyer["stockId"])
    else:
        # Order price = current stock price
        # Refund buyer their difference from the current price
        supabase_middleman.sell_stock(seller["userId"], seller["stockId"], curr_price)
        supabase_middleman.buy_stock(buyer["userId"], buyer["stockId"])
        supabase_middleman.resolve_price_diff(buyer["userId"], buy_diff)

    # Deletes sell order used in the active_buy_sell table
    supabase_middleman.delete_processed_order(seller["Id"])
    # Logs transaction in the inactive_buy_sell table
    supabase_middleman.log_transaction(buyer, seller)
    return "Conducted and logged transaction"
