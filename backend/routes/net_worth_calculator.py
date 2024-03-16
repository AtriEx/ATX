"""API handler for calculating the net worth of a user"""

import os

from dotenv import load_dotenv

from supabase import Client, create_client

from database import supabase_middleman

load_dotenv("env/.env")


url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def net_worth_calculator(user_id: str) -> int:
    """
    Gets the user's networth from profile, portfolio, and active_buy_sell

    Args:
        user_id (int): The id of the user whose net worth is requested

    Returns: Net worth of user
    """

    # Get the user's balance
    profile_balance = (supabase.table("profiles")
        .select("balance")
        .match({"userId": user_id})
        .execute()
        .data
        .pop()["balance"])

    # Get the user's portfolio
    user_portfolio = (supabase.table("portfolio")
        .select("quantity,stockId")
        .match({"userId": user_id})
        .execute()
        .data)
    portfolio_balance = 0

    # Calculate the value of the user's portfolio
    for stock in user_portfolio:
        portfolio_balance += stock["quantity"] * supabase_middleman.fetch_stock_price(stock["stockId"])

    # Get the user's active buy/sell orders
    active_buy_sell_entries = (supabase.table("active_buy_sell")
        .select("price,quantity,stockId,buy_or_sell,userId")
        .match({"userId": user_id})
        .execute()
        .data)
    
    # Calculate the value of the user's active buy/sell orders
    active_order_balance = 0
    for entry in active_buy_sell_entries:
        if entry["buy_or_sell"]:
            active_order_balance += entry["price"] * entry["quantity"] # buy order
        else:
            active_order_balance += supabase_middleman.fetch_stock_price(entry["stockId"]) * entry["quantity"] # sell order

    return active_order_balance + portfolio_balance + profile_balance
   
