"""Supabase middleman should contain all of the database 
interactions in high-level generic functions."""

import os
from datetime import datetime

from dotenv import load_dotenv
from supabase import Client, create_client

# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root

load_dotenv("env/.env")
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


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
        .data.pop()
    )
    return is_open["state"]


def update_user_balance(user_id: str, amount: int) -> int:
    """
    Updates the user's balance by adding the given amount

    Args:
        user_id (str): The user's ID
        amount (int): The amount to add to the user's balance

    Returns: int - The new balance
    """
    old_balance = (
        supabase.table("profiles")
        .select("balance")
        .eq("userId", user_id)
        .execute()
        .data.pop()["balance"]
    )
    new_balance = (
        supabase.table("profiles")
        .update({"balance": old_balance + amount})
        .eq("userId", user_id)
        .execute()
    )
    # make sure in the future that the query executed correctly and return if it didn't
    return new_balance


def update_user_portfolio(user_id: str, stock_id: int, quantity: int) -> int:
    """
    Updates the user's portfolio by adding the given quantity of the stock

    Args:
        user_id (str): The user's ID
        stock_id (int): The stock's ID
        quantity (int): The quantity of the stock to add

    Returns: int - The new quantity of the stock in the user's portfolio
    """
    result = (
        supabase.table("portfolio")
        .select("quantity")
        .eq("userId", user_id)
        .eq("stockId", stock_id)
        .execute()
        .data
    )
    if result:
        old_quantity = result.pop()["quantity"]
        new_quantity = (
            supabase.table("portfolio")
            .update({"quantity": old_quantity + quantity})
            .eq("userId", user_id)
            .eq("stockId", stock_id)
            .execute()
        )
        payload = new_quantity
    else:
        supabase.table("portfolio").insert(
            {"userId": user_id, "stockId": stock_id, "quantity": quantity}
        ).execute()
        payload = quantity
    return payload


def fetch_stock_price(stock_id: int) -> int:
    """
    Gets the current stock price of the given stock_id

    Args:
        stock_id (int): The id of the stock you want to get the price of

    Returns: The price of the stock
    """

    result = (
        supabase.table("stock_price")
        .select("stock_price")
        .eq("stockId", stock_id)
        .execute()
        .data
    )

    if result:
        stock_price = result.pop()["stock_price"]
        return stock_price
    return None


def delete_processed_order(order_index: int) -> None:
    """
    Deletes the sell/buy order fufilled in a transaction from the active_buy_sell table

    Args:
        order_index(int): The unique row identifier for an entry in the active_buy_sell table

    Returns: None
    """
    print(order_index)
    supabase.table("active_buy_sell").delete().eq("Id", order_index).execute()


def log_transaction(buy_info: dict, sell_info: dict) -> None:
    """
    Logs tansaction info in the inactive_buy_sell table (Should be called @ the end of order flow)
    Removes the Id column from the buyer & seller info before logging the transaction

    Args:
        buy_info (dict): Data related to the buy side of the transaction
        sell_info (dict): Data relatedto the sell side of the transaction

    Returns: None
    """

    del buy_info["Id"]
    del buy_info["has_been_processed"]
    del sell_info["Id"]
    del sell_info["has_been_processed"]

    supabase.table("inactive_buy_sell").insert(buy_info).execute()
    supabase.table("inactive_buy_sell").insert(sell_info).execute()


def get_expired() -> list[dict]:
    """
    Return a list of active orders that have expired.
    Only contains the order id.
    """

    orders = (
        supabase.table("active_buy_sell")
        .select("Id")
        .lte("expirey", datetime.now().isoformat())
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
    