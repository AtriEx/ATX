"""API handler for creating and fulfilling buy orders."""

import os
from datetime import datetime, timedelta

from database import supabase_middleman
from dotenv import load_dotenv

# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root
from supabase import Client, create_client

load_dotenv()

url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def buy_order():
    """Create a buy order for one share of a stock
    and fullfill it if possible."""
    # Return state by looking for the one with the biggest ID
    is_open = supabase_middleman.is_market_open()
    if not is_open:
        # If the market is closed
        return "The market is closed"

    buy_info = {
        "userId": "572a902e-de7a-4739-adfe-f4af32a3f18b",
        "buy_or_sell": True,
        "stockId": 2,
        "price": 15,
        "quantity": 1,
        "time_posted": datetime.now().isoformat(),
        "expirey": (
            datetime.now() + timedelta(hours=1)
        ).isoformat(),  # This is a test value; users will input an expiry date
    }

    # If the market is open, get all active sells for the stock <= buy_price, ordered by price
    valid_sells = (
        supabase.table("active_buy_sell")
        .select("*")
        .match({"buy_or_sell": False, "stockId": buy_info["stockId"]})
        .lte("price", buy_info["price"])
        .order("price")
        .execute()
        .data
    )
    if not valid_sells:
        # Insert the buy order into active_buy_sell if it can't be fufilled
        # supabaseMiddleman.log_unfulfilled_buy(buy_info)
        return "No valid sale for this transaction"

    # cheapest_sale = valid_sells[0]
    # saleId = cheapest_sale["Id"]
    # sell_info = {"userId": cheapest_sale["userId"],
    #             "buy_or_sell": False,
    #             "stockId": cheapest_sale["stockId"],
    #             "price": cheapest_sale["price"],
    #             "quantity": 1,
    #             "time_posted": cheapest_sale["time_posted"],
    #             "expirey": cheapest_sale["expirey"]
    #             }
    # # Get Buyer and Seller user info and their holdings of the stock being traded
    # buyer_profile = supabase_middleman.fetch_profile(buy_info["userId"])
    # buyer_portfolio = supabase_middleman.fetch_portfolio(buy_info["userId"], buy_info["stockId"])
    # seller_profile = supabase_middleman.fetch_profile(sell_info["userId"])
    # seller_portfolio = supabase_middleman.fetch_portfolio(
    #     sell_info["userId"], sell_info["stockId"]
    # )
    return "Transaction profiles and portfolios fetched"

    # Exchange the stock by altering balances and stock holdings of buyer & seller
    # (disabled for testing)
    # supabase_middleman.exchange_stock(
    #     buyer_profile, buyer_portfolio, seller_profile, seller_portfolio, sell_price
    # )

    # Log the transactions by inserting them into the inactive_buy_sell table
    # supabaseMiddleman.log_transaction(buy_info, sell_info)

    # Delete active sell order that was just fufilled (disabled for testing)
    # supabase.table("active_buy_sell").delete().eq("id",saleId)
