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


def log_transaction(buy_info: dict, sell_info: dict) -> None:
    """
    Logs buy and sell tansaction info in the inactive_buy_sell

    Args:
        buy_info (dict): Data related to the buy side of the transaction
        sell_info (dict): Data relatedto the sell side of the transaction

    Returns: None
    """
    supabase.table("inactive_buy_sell").insert(buy_info).execute()
    supabase.table("inactive_buy_sell").insert(sell_info).execute()


# unreviewed
def log_unfulfilled_buy(order_info: dict) -> None:
    """
    Logs info of a order if it cannot be fulfilled

    Args:
        order_info (dict): Data related to the buy side of a transaction

    Returns: None
    """
    supabase.table("active_buy_sell").insert(order_info).execute()


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

    supabase.table("portfolio").update({"quantity": seller_quantity - 1}).match({"userId": user_id, "stockId": stock_id})
    supabase.table("profiles").update({"balance": seller_balance + order_price}).eq("userId", user_id)


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

    buyer_stock = (supabase.table("portfolio")
                   .select("quantity")
                   .match({"userId": user_id, "stockId": stock_id})
                   .execute()
                   .data
                   .pop()
                   )

    buyer_profile = (supabase.table("profiles")
                     .select("balance")
                     .eq("userId", user_id)
                     .execute()
                     .data
                     .pop()
                     )

    buyer_quantity = buyer_stock["quantity"]
    buyer_balance = buyer_profile["balance"]

    supabase.table("portfolio").update({"quantity": buyer_quantity + 1}).match({"userId": user_id, "stockId": stock_id})
    supabase.table("profiles").update({"balance": buyer_balance - order_price}).eq("userId", user_id)


def resolve_price_diff(user_id: str, price_diff: int) -> None:
    """
    Handles difference in desired prices between the buyer and seller

    Args:
        user_id: The user who's balance will be handled
        price_diff: The amount to be refunded/ rewarded back to the user

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
    supabase.table("profiles").update({"balance": user_balance + price_diff}).eq("userId", user_id)
