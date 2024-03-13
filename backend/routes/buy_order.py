"""API handler for creating and fulfilling buy orders."""

import os
<<<<<<< HEAD
<<<<<<< HEAD
from util import test_data
from database import supabase_middleman
=======
from datetime import datetime, timedelta

>>>>>>> a9dd20a (enforce black formatting style)
=======
>>>>>>> 15dc317 (linter changes)
from dotenv import load_dotenv
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> aa61e28 (test commit of black formatting)
# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root
=======
>>>>>>> 914805c (remove unnecessary linter disables)
from supabase import Client, create_client
from database import supabase_middleman

<<<<<<< HEAD
load_dotenv("env/.env")
=======
from database import supabase_middleman

load_dotenv()
>>>>>>> a9dd20a (enforce black formatting style)

url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def test_params():
    """API route for testing parameters."""
    return "Test parameters"


def buy_order(data: dict) -> str:
    """Create a buy order for one share of a stock
    and fullfill it if possible."""
    # These are test values
    # We will have a function that returns this data using API call parameters
    buyer = data
    # Slects all active sells order by price then by time-posted (desc)
    valid_sells = (
        supabase.table("active_buy_sell")
        .select(
            "Id",
            "userId",
            "time_posted",
            "buy_or_sell",
            "price",
            "quantity",
            "stockId",
            "orderId",
            "has_been_processed",
        )
        .match(
            {
                "buy_or_sell": False,
                "stockId": buyer["stockId"],
                "has_been_processed": True,
            }
        )
        .lte("price", buyer["price"])
        .order("price", desc=False)
        .order("time_posted")
        .limit(1)
        .execute()
        .data
    )
    # Market is open and a valid sell is availible
    if not valid_sells:
        # Insert the buy order into active_buy_sell if it can't be fufilled
        # supabase_middleman.log_unfulfilled_order(buyer)
        supabase.table("active_buy_sell").update({"has_been_processed": True}).match(
            {"Id": buyer["Id"]}
        ).execute()
        return "No valid sells"

    # Gets sell order closest to the buy price
    seller = valid_sells.pop()
    # Finds the distances between the current price and the buy/sell prices
    # Decides order handling based off which price is closest to current price
    curr_price = supabase_middleman.fetch_stock_price(seller["stockId"])
    # the difference between the current price and the sellers price
    sell_diff = abs(curr_price - seller["price"])
    # the difference between the current price and the buyers price
    buy_diff = abs(buyer["price"] - curr_price)
    # the difference between the buyers price and the sellers price
    order_diff = buyer["price"] - seller["price"]
    # Checks edge case where buy price = sell price != current market price
    if order_diff == 0:
        # Order can be fulfilled @ price of both buyer and seller, no refund required.
        supabase_middleman.update_user_balance(seller["userId"], seller["price"])
        supabase_middleman.update_user_portfolio(
            buyer["userId"], buyer["stockId"], buyer["quantity"]
        )
        payload = "Order fulfilled at desired price"
    elif sell_diff < buy_diff:
        # Order price=sell price; refund the difference between buy and sell price to the buyer
        # top row from excalidraw
        supabase_middleman.update_user_balance(seller["userId"], seller["price"])
        supabase_middleman.update_user_balance(buyer["userId"], order_diff)
        supabase_middleman.update_user_portfolio(
            buyer["userId"], buyer["stockId"], buyer["quantity"]
        )
        payload = "Order fulfilled at sellers price. refund issued to buyer"
    elif buy_diff < sell_diff:
        # Order price = buy price; No refund needed because seller will sell @ higher price
        # is the same as the first condition, but kept in for clarity
        # middle row from excalidraw
        supabase_middleman.update_user_balance(seller["userId"], buyer["price"])
        supabase_middleman.update_user_portfolio(
            buyer["userId"], buyer["stockId"], buyer["quantity"]
        )
        payload = "Order fulfilled at buyers price. No refund needed."
    else:
        # Order price = current stock price
        # Refund buyer their difference from the current price
        # bottom row from excalidraw
        supabase_middleman.update_user_balance(seller["userId"], curr_price)
        supabase_middleman.update_user_balance(buyer["userId"], buy_diff)
        supabase_middleman.update_user_portfolio(
            buyer["userId"], buyer["stockId"], buyer["quantity"]
        )
        payload = "Order fulfilled at current price. Refund issued to buyer."

    # Deletes sell order used in the active_buy_sell table
    supabase_middleman.delete_processed_order(seller["Id"])
    supabase_middleman.delete_processed_order(buyer["Id"])
    # Logs transaction in the inactive_buy_sell table
    supabase_middleman.log_transaction(buyer, seller)
    return payload
