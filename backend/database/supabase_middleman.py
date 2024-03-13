"""Supabase middleman should contain all of the database 
interactions in high-level generic functions."""

import os
from datetime import datetime

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv("env/.env")
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def fetch_entries():
    """
    Fetches all entries from a table
    """


# needs a lot more checks and error handling
def insert_entry(table_name: str, entry: dict) -> None:
    """
    Inserts an entry into a table

    Args:
        table_name (str): The name of the table
        entry (dict): The entry to be inserted

    Returns: None
    """
    supabase.table(table_name).insert(entry).execute()


def is_market_open() -> bool:
    """
    Checks if the market is open

    Returns: True if the market is open, False otherwise
    """
    is_open = (
        supabase.table("market_State")
        .select("state")
        .order("id", desc=True)
        .limit(1)
        .execute()
        .data
    )
    return is_open


def fetch_profile(user_id: str) -> dict:
    """
    Fetches user data from profiles table using userId

    Args:
        user_id (str): The ID of the user

    Returns: profile dictionary
    """

    return (
        supabase.table("profiles").select("*").eq("userId", user_id).execute().data[0]
    )


# unreviewed
def fetch_portfolio(user_id: str, stock_id: int) -> dict:
    """
    Fetches stock data from portfolio table using userID and stockID

    Args:
        user_id (str): The ID of the user
        stock_id (int): The ID of the stock

    Returns: Dictionary describing a user's holding of a stock
    """
    portfolios = (
        supabase.table("portfolio")
        .select("*")
        .match({"userId": user_id, "stockId": stock_id})
        .execute()
        .data
    )
    if portfolios:
        return portfolios[0]

    stock = (
        supabase.table("stock_price")
        .select("stock_price")
        .eq("stockId", stock_id)
        .execute()
        .data
    )
    portfolio = (
        supabase.table("portfolio")
        .select("portfolio_ID")
        .eq("userId", user_id)
        .order("portfolio_ID", desc=True)
        .limit(1)
        .execute()
        .data
    )
    if not stock:
        stock = [{"stock_price": 0}]
    if not portfolio:
        portfolio = [{"portfolio_ID": 0}]

    stock = stock[0]
    portfolio = portfolio[0]
    return {
        "stockId": stock_id,
        "quantity": 0,
        "userId": user_id,
        "Price": stock["stock_price"],
        "portfolio_ID": portfolio["portfolio_ID"] + 1,
    }


# unreviewed
def exchange_stock(
    buyer_profile: dict,
    buyer_portfolio: dict,
    seller_profile: dict,
    seller_portfolio: dict,
    stock_price: float,
) -> None:
    """
    Updates buyer and seller profiles & portfolios when a stock is transacted

    Args:
        buyer_profile (dict): The buyer's profile data, includes balance and net worth
        buyer_portfolio (dict): Data related to the buyer's holdings of a certain stock
        seller_profile (dict): The seller's profile data, includes balance and net worth
        seller_portfolio (dict): Data related to the seller's holdings of a certain stock
        stock_price (float): The curent sell price of the transacted stock

    Returns: None
    """
    buyer_portfolio["quantity"] += 1
    supabase.table("portfolio").upsert(buyer_portfolio)
    supabase.table("profiles").update(
        {"balance": buyer_profile["balance"] - stock_price}
    ).eq("userId", buyer_profile["userId"])

    seller_portfolio["quantity"] -= 1
    supabase.table("portfolio").upsert(seller_portfolio)
    supabase.table("profiles").update(
        {"balance": seller_profile["balance"] + stock_price}
    ).eq("userId", seller_profile["userId"])


# unreviewed
def log_transaction(buy_info: dict, sell_info: dict) -> None:
    """
    Logs buy and sell tansaction info in the inactive_buy_sell

    Args:
        buy_info (dict): Data related to the buy side of the transaction
        sell_info (dict): Data relatedto the sell side of the transaction

    Returns: None
    """
    latest_row = (
        supabase.table("inactive_buy_sell")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
        .data
    )
    latest_id = latest_row[0]["id"]

    latest_id += 1
    supabase.table("inactive_buy_sell").insert(
        {
            "id": latest_id,
            "delisted_time": datetime.now().isoformat(),
            "userId": buy_info["buyerId"],
            "buy_or_sell": buy_info["buy_or_sell"],
            "time_posted": buy_info["time_posted"],
            "price": buy_info["price"],
            "expirey": buy_info["expirey"],
            "quantity": buy_info["quantity"],
            "completed": True,
            "stockId": buy_info["stockId"],
        }
    ).execute()

    latest_id += 1
    supabase.table("inactive_buy_sell").insert(
        {
            "id": latest_id,
            "delisted_time": datetime.now().isoformat(),
            "userId": sell_info["sellerId"],
            "buy_or_sell": sell_info["buy_or_sell"],
            "time_posted": sell_info["time_posted"],
            "price": sell_info["price"],
            "expirey": sell_info["expirey"],
            "quantity": sell_info["quantity"],
            "completed": True,
            "stockId": sell_info["stockId"],
        }
    ).execute()


# unreviewed
def log_unfulfilled_buy(buy_info: dict) -> None:
    """
    Logs info of a buy order if it cannot be fulfilled

    Args:
        buy_info (dict): Data related to the buy side of a transaction

    Returns: None
    """
    latest_row = (
        supabase.table("active_buy_sell")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
        .data
    )
    latest_id = latest_row[0]["id"]

    latest_id += 1
    supabase.table("active_buy_sell").insert(
        {
            "id": latest_id,
            "time_posted": buy_info["time_posted"],
            "buy_or_sell": buy_info["buy_or_sell"],
            "price": buy_info["price"],
            "expirey": buy_info["expirey"],
            "qunatity": buy_info["qunatity"],
            "stockId": buy_info["stockId"],
            "userId": buy_info["userId"],
        }
    ).execute()


def get_active() -> list[dict]:
    """
    Return active buy orders (only their expiry time and id),
    sorted by their expiry time (ascending)
    """

    orders = (
        supabase.table("active_buy_sell")
        .select("Id,expirey")
        .order("expirey", desc=False)
        .execute()
    )

    return orders.data


def expire_order(order_id: int):
    """
    Move order_id from active to inactive order table
    Refunds stocks or money

    Args:
        order_id (int): The active order id
    """

    # Delete order
    order = (
        supabase.table("active_buy_sell").delete().eq("Id", order_id).execute()
    ).data[0]

    # Refund stocks/money
    if order["buy_or_sell"]:
        # Buy order - refund money
        order_cost = order["quantity"] * order["price"]

        current_balance = (
            supabase.table("profiles")
            .select("balance")
            .eq("userId", order["userId"])
            .single()
            .execute()
        ).data["balance"]

        supabase.table("profiles").update({"balance": current_balance + order_cost}).eq(
            "userId", order["userId"]
        ).execute()

    else:
        # Sell order - refund stock
        supabase.table("portfolio").insert(
            {
                "stockId": order["stockId"],
                "userId": order["userId"],
                "quantity": order["quantity"],
                "price_avg": order["price"],
            }
        ).execute()

    # Insert record into inactive_buy_sell
    del order["has_been_processed"]
    order["delisted_time"] = datetime.now().isoformat()

    supabase.table("inactive_buy_sell").insert(order).execute()


def update_entry():
    """
    Updates an entry in a table
    """
