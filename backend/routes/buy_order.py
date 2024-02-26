"""API handler for creating and fulfilling buy orders."""

import os
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
    buy_info = test_data.test_entry_1()
    # Return state by looking for the one with the biggest ID
    is_open = supabase_middleman.is_market_open()
    if not is_open:
        # If the market is closed
        supabase_middleman.log_unfulfilled_order(buy_info)
        return "The market is closed"

    # If the market is open, get all active sells for the stock <= buy_price
    # Active sells are ordered by price and time_posted (descending)
    valid_sells = (
        supabase.table("active_buy_sell")
        .select("*")
        .match({"buy_or_sell": False, "stockId": buy_info["stockId"]})
        .lte("price", buy_info["price"])
        .order("price")
        .order("time_posted", desc=True)
        .execute()
        .data
    )
    if not valid_sells:
        # Insert the buy order into active_buy_sell if it can't be fufilled
        supabase_middleman.log_unfulfilled_order(buy_info)
        return "No valid sale for this transaction"

    # Gets sell order closest to the buy price
    sell_info = valid_sells.pop()
    # Finds the distances between the current price and the buy/sell prices
    # Decides order handling based off which price is closest to current price
    curr_stock_price = supabase_middleman.fetch_stock_price(sell_info["stockId"])
    sell_diff = abs(curr_stock_price - sell_info["price"])
    buy_diff = abs(buy_info["price"] - curr_stock_price)
    order_diff = buy_info["price"] - sell_info["price"]
    # Checks edge case where buy price = sell price != current market price
    if (order_diff == 0) and (buy_info["price"] != curr_stock_price):
        # Order cannot be fulfilled @ current price
        supabase_middleman.log_unfulfilled_order(buy_info)
        return "Current stock price didn't match equal buy & sell prices"

    if sell_diff < buy_diff:
        # Order price = sell price; refund the difference between buy and sell price to the buyer
        supabase_middleman.sell_stock(sell_info["userId"], sell_info["stockId"], sell_info["price"])
        supabase_middleman.buy_stock(buy_info["userId"], buy_info["stockId"], sell_info["price"])
        supabase_middleman.resolve_price_diff(buy_info["userId"], order_diff)
    elif buy_diff < sell_diff:
        # Order price = buy price; No refund needed because seller will sell @ higher price
        supabase_middleman.sell_stock(sell_info["userId"], sell_info["stockId"], buy_info["price"])
        supabase_middleman.buy_stock(buy_info["userId"], buy_info["stockId"], buy_info["price"])
    else:
        # Order price = current stock price
        # Refund buyer and seller their difference from the current price
        supabase_middleman.sell_stock(sell_info["userId"], sell_info["stockId"], curr_stock_price)
        supabase_middleman.buy_stock(buy_info["userId"], buy_info["stockId"], curr_stock_price)
        supabase_middleman.resolve_price_diff(buy_info["userId"], buy_diff)
        supabase_middleman.resolve_price_diff(sell_info["userId"], sell_diff)

    # Deletes sell order used in the active_buy_sell table
    supabase_middleman.delete_processed_order(sell_info["Id"])
    # Logs transaction in the inactive_buy_sell table
    supabase_middleman.log_transaction(buy_info, sell_info)
    return "Conducted and logged transaction; deleted active order"
