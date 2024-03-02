"""Supabase middleman should contain all of the database 
interactions in high-level generic functions."""

import os
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


# unreviewed
def escrow_buy(user_id: str, buy_price: int) -> None:
    """
    Subtracts given buy order price from user's balance

    Args:
        buy_price(int): The price submitted by the buyer
        user_id(str): The buyer's user ID
    Returns: None
    """

    supabase.rpc("update_balance", {"user_id": user_id, "price_delta": (-1*buy_price)}).execute()


# unreviewed
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


# unreviewed
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
    supabase.rpc("sell_stock",
                 {"user_id": user_id, "stock_id": stock_id, "order_price": order_price}
                 ).execute()


# unreviewed
def buy_stock(user_id: str, stock_id: int) -> None:
    """
    Buys a stock for the user_id stock at the order_price
    (Assumes the user has a portfolio of that stock)

    Args:
        user_id (str): The user on the buy side of a stock transaction
        stock_id(int): The ID of the stock being bought
        order_price(int): Price closest to current stock price presented by the buyer or seller

    Returns: None
    """
    supabase.rpc("buy_stock", {"user_id": user_id, "stock_id": stock_id}).execute()


# unreviewed
def resolve_price_diff(user_id: str, price_diff: int) -> None:
    """
    Handles difference in desired prices between the buyer and seller

    Args:
        user_id(str): The user who's balance will be handled
        price_diff(int): The amount to be refunded/ rewarded back to the user

    Returns: None
    """
    supabase.rpc("update_balance", {"user_id": user_id, "price_delta": price_diff}).execute()


# unreviewed
def delete_processed_order(order_index: int) -> None:
    """
    Deletes the sell/buy order fufilled in a transaction from the active_buy_sell table

    Args:
        order_index(int): The unique row identifier for an entry in the active_buy_sell table

    Returns: None
    """
    print(order_index)
    supabase.table("active_buy_sell").delete().eq("Id", order_index).execute()


# unreviewed
def log_transaction(buy_info: dict, sell_info: dict) -> None:

    """
    Logs tansaction info in the inactive_buy_sell table (Should be called @ the end of order flow)
    Removes the Id column from the buyer & seller info before logging the transaction

    Args:
        buy_info (dict): Data related to the buy side of the transaction
        sell_info (dict): Data relatedto the sell side of the transaction

    Returns: None
    """
    if buy_info.get("Id"):
        del buy_info["Id"]
    if buy_info.get("has_been_processed") is not None:
        del buy_info["has_been_processed"]
    if sell_info.get("Id"):
        del sell_info["Id"]
    if sell_info.get("has_been_processed") is not None:
        del sell_info["has_been_processed"]

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
    if order_info.get("has_been_processed") is not None:
        del order_info["has_been_processed"]
    supabase.table("active_buy_sell").insert(order_info).execute()
def networth_calculator(user_id: str) -> int:
    
 #this gets the balance from the profile table  
    profile_balance= (supabase.table('profiles')
    .select('balance')
    .match({"userId":user_id})
    .execute()
    .data
    .pop()["balance"])
 #this gets the stock from portfolio and and multiply it by the price from the stock_price table
    user_portfolio=(supabase.table('portfolio')
    .select('quantity,stockId')
    .match({"userId":user_id})
    .execute()
    .data)
    portfolio_balance=0
    for stock in user_portfolio:
        portfolio_balance+= stock["quantity"]* fetch_stock_price(stock["stockId"])
 #idk
    active_buy_sell_entries=(supabase.table('active_buy_sell')
    .select('price,quantity,stockId,buy_or_sell,userId')
    .match({"userId":user_id})
    .execute()
    .data)
    buy_balance=0
    sell_balance=0
    for entry in active_buy_sell_entries:
        if entry["buy_or_sell"]==True:
            buy_balance+= (entry['price']*entry["quantity"])
        else:
            sell_balance+=(fetch_stock_price(entry["stockId"])*entry["quantity"])
    return sell_balance
 #then I add all the values here and return them
    return profile_balance+portfolio_balance
   

