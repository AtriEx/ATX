"""Supabase middleman should contain all of the database 
interactions in high-level generic functions."""

import os
from datetime import datetime

from dotenv import load_dotenv

# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root
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
        .pop()
    )
    return is_open["state"]


def update_entry():
    """
    Updates an entry in a table
    """


def fetch_stock_price(stock_id: int) -> int:
    """
    Gets the current stock price of the given stock_id

    Args:
        stock_id (int): The id of the stock you want to get the price of

    Returns: The price of the stock 
    """

    stock_price = (supabase.table("stock_price")
                   .select("stock_price")
                   .eq("stockId", stock_id)
                   .execute()
                   .data
                   .pop()
                   )
    return stock_price["stock_price"]


def sell_stock(user_id: str, stock_id: int, order_price: int) -> None:
    """
    Sells a user's stock at the order_price
    (Assumes the user has a portfolio of that stock)

    Args:
        user_id (str): The user on the sell side of a stock transaction
        stock_id(int): The ID of the stock being sold
        order_price(int): Price closest to current stock price presented by the buyer or seller

    Returns: None
    """

    seller_stock = (supabase.table("portfolio")
                    .select("quantity")
                    .match({"userId": user_id, "stockId": stock_id})
                    .execute()
                    .data
                    .pop()
                    )
    seller_profile = (supabase.table("profiles")
                      .select("balance")
                      .eq("userId", user_id)
                      .execute()
                      .data
                      .pop()
                      )

    seller_quantity = seller_stock["quantity"]
    seller_balance = seller_profile["balance"]

    supabase.table("portfolio").update({"quantity": seller_quantity - 1}).match({"userId": user_id, "stockId": stock_id}).execute()
    supabase.table("profiles").update({"balance": seller_balance + order_price}).eq("userId", user_id).execute()


def buy_stock(user_id: str, stock_id: int, order_price: int) -> None:
    """
    Buys a stock for the user_id stock at the order_price
    (Assumes the user has a portfolio of that stock)

    Args:
        user_id (str): The user on the buy side of a stock transaction
        stock_id(int): The ID of the stock being bought
        order_price(int): Price closest to current stock price presented by the buyer or seller

    Returns: None
    """
    buyer_profile = (supabase.table("profiles")
                     .select("balance")
                     .eq("userId", user_id)
                     .execute()
                     .data
                     .pop()
                     )
    buyer_stock = (supabase.table("portfolio")
                   .select("quantity")
                   .match({"userId": user_id, "stockId": stock_id})
                   .execute()
                   .data
                   )
    # Handles the case where the user doesn't have an entry for that stock yet in the portfolio table
    if not buyer_stock:
        buyer_stock = {"userId": user_id, "stockId": stock_id, "quantity": 0, "price_avg": float(0)}
        supabase.table("portfolio").insert(buyer_stock).execute()
    else:
        buyer_stock = buyer_stock.pop()

    buyer_quantity = buyer_stock["quantity"]
    buyer_balance = buyer_profile["balance"]

    supabase.table("portfolio").update({"quantity": buyer_quantity + 1}).match({"userId": user_id, "stockId": stock_id}).execute()
    supabase.table("profiles").update({"balance": buyer_balance - order_price}).eq("userId", user_id).execute()


def resolve_price_diff(user_id: str, price_diff: int) -> None:
    """
    Handles difference in desired prices between the buyer and seller

    Args:
        user_id(str): The user who's balance will be handled
        price_diff(int): The amount to be refunded/ rewarded back to the user

    Returns: None
    """

    user_profile = (supabase.table("profiles")
                    .select("balance")
                    .eq("userId", user_id)
                    .execute()
                    .data
                    .pop()
                    )

    user_balance = user_profile["balance"]
    supabase.table("profiles").update({"balance": user_balance + price_diff}).eq("userId", user_id).execute()


def delete_processed_order(order_index) -> None:
    """
    Deletes the sell/buy order fufilled in a transaction from the active_buy_sell table

    Args:
        order_index(dict): The unique row identifier for an entry in the active_buy_sell table

    Returns: None
    """
    supabase.table("active_buy_sell").delete().eq("Id", order_index).execute()


# unreviewed
def log_transaction(buy_info: dict, sell_info: dict) -> None:
    """
    Logs buy and sell tansaction info in the inactive_buy_sell (Should be called @ the end of order flow)
    Removes the Id column from the buyer & seller info as a preprocessing step before logging the transaction

    Args:
        buy_info (dict): Data related to the buy side of the transaction
        sell_info (dict): Data relatedto the sell side of the transaction

    Returns: None
    """
    if buy_info.get("Id"):
        del buy_info["Id"]
    if sell_info.get("Id"):
        del sell_info["Id"]

    supabase.table("inactive_buy_sell").insert(buy_info).execute()
    supabase.table("inactive_buy_sell").insert(sell_info).execute()


# unreviewed
def log_unfulfilled_order(order_info: dict) -> None:
    """
    Logs info of a order if it cannot be fulfilled (Should be called @ the end of order flow)
    Removes the Id column from the order info as a preprocessing step before logging the order

    Args:
        order_info (dict): Data related to the buy side of a transaction

    Returns: None
    """
    if order_info.get("Id"):
        del order_info["Id"]
    supabase.table("active_buy_sell").insert(order_info).execute()
