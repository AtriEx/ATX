"""Supabase middleman should contain all of the database 
interactions in high-level generic functions."""

import os
from datetime import datetime

from dotenv import load_dotenv
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> aa61e28 (test commit of black formatting)
=======
from supabase import Client, create_client  
>>>>>>> 03b6667 (fixed some of the errors i introduced in the merge)
# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root
=======
>>>>>>> a9dd20a (enforce black formatting style)
=======
>>>>>>> 81e8d77 (more linter fixes)
=======

>>>>>>> c51a102 (more linter fixes)
=======
>>>>>>> 1f2d31f (more linter fixes maybe)
=======
=======
# pylint: disable=import-error,no-name-in-module # it"s looking in the supabase folder in project root
>>>>>>> 8bc8647 (reformatting/refactoring)
>>>>>>> 9fdc647 (reformatting/refactoring)
=======
=======
# pylint: disable=import-error,no-name-in-module # it"s looking in the supabase folder in project root
>>>>>>> 8bc8647 (reformatting/refactoring)
=======
# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root
>>>>>>> 9f154e1 (changed typos)
>>>>>>> 796bd58 (changed typos)
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
<<<<<<< HEAD
    Updates the user's balance by adding the given amount

    Args:
        user_id (str): The user's ID
        amount (int): The amount to add to the user's balance

    Returns: int - The new balance
=======
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
>>>>>>> 8bc8647 (reformatting/refactoring)
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


<<<<<<< HEAD
<<<<<<< HEAD



<<<<<<< HEAD
=======
=======
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

>>>>>>> 9fdc647 (reformatting/refactoring)
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
        user_id(str): The user who"s balance will be handled
        price_diff(int): The amount to be refunded/ rewarded back to the user

    Returns: None
    """
    supabase.rpc("update_balance", {"user_id": user_id, "price_delta": price_diff}).execute()


# unreviewed
<<<<<<< HEAD
=======
>>>>>>> 4f518fb (fixed changes from code walkthrough)
=======
>>>>>>> aa61e28 (test commit of black formatting)
=======
>>>>>>> 8bc8647 (reformatting/refactoring)
>>>>>>> 9fdc647 (reformatting/refactoring)
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
<<<<<<< HEAD
<<<<<<< HEAD



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
    """
    Gets the user's networth from profile, portfolio, and active_buy_sell test

    Args:
        user_id (int): The id of the user whose net worth is requested

    Returns: Net worth of user
    """
    profile_balance = (supabase.table("profiles")
        .select("balance")
        .match({"userId": user_id})
        .execute()
        .data
        .pop()["balance"])

    user_portfolio = (supabase.table("portfolio")
        .select("quantity,stockId")
        .match({"userId": user_id})
        .execute()
        .data)
    portfolio_balance = 0
    for stock in user_portfolio:
        portfolio_balance += stock["quantity"] * fetch_stock_price(stock["stockId"])

    active_buy_sell_entries = (supabase.table("active_buy_sell")
        .select("price,quantity,stockId,buy_or_sell,userId")
        .match({"userId": user_id})
        .execute()
        .data)
    active_order_balance = 0
    for entry in active_buy_sell_entries:
        if entry["buy_or_sell"]:
            active_order_balance += entry["price"] * entry["quantity"]
        else:
            active_order_balance += fetch_stock_price(entry["stockId"]) * entry["quantity"]

<<<<<<< HEAD
<<<<<<< HEAD
    return active_order_balance + portfolio_balance + profile_balance
   

=======
>>>>>>> aa61e28 (test commit of black formatting)
=======
def get_active() -> list[dict]:
=======
=======


>>>>>>> 81e8d77 (more linter fixes)
def get_expired() -> list[dict]:
>>>>>>> f827511 (:thread: Change from asyncio to threading)
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
<<<<<<< HEAD

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD


def update_entry():
    """
    Updates an entry in a table
    """
>>>>>>> 1d67bff (✨ Get active orders sorted by expiry)
=======
    
>>>>>>> 81e8d77 (more linter fixes)
=======
>>>>>>> 1f2d31f (more linter fixes maybe)
=======
=======
=======
    if order_info.get("Id"):
        del order_info["Id"]
    if order_info.get("has_been_processed") is not None:
        del order_info["has_been_processed"]
    supabase.table("active_buy_sell").insert(order_info).execute()

>>>>>>> 8bc8647 (reformatting/refactoring)
>>>>>>> 9fdc647 (reformatting/refactoring)
def networth_calculator(user_id: str) -> int:
    """
    Gets the user's networth from profile, portfolio, and active_buy_sell

    Args:
        user_id (int): The id of the user whose net worth is requested

    Returns: Net worth of user
    """
    profile_balance = (supabase.table("profiles")
        .select("balance")
        .match({"userId": user_id})
        .execute()
        .data
        .pop()["balance"])

    user_portfolio = (supabase.table("portfolio")
        .select("quantity,stockId")
        .match({"userId": user_id})
        .execute()
        .data)
    portfolio_balance = 0
    for stock in user_portfolio:
        portfolio_balance += stock["quantity"] * fetch_stock_price(stock["stockId"])

    active_buy_sell_entries = (supabase.table("active_buy_sell")
        .select("price,quantity,stockId,buy_or_sell,userId")
        .match({"userId": user_id})
        .execute()
        .data)
    active_order_balance = 0
    for entry in active_buy_sell_entries:
        if entry["buy_or_sell"]:
            active_order_balance += entry["price"] * entry["quantity"]
        else:
            active_order_balance += fetch_stock_price(entry["stockId"]) * entry["quantity"]

    return active_order_balance + portfolio_balance + profile_balance
   

>>>>>>> cfd74d4 (what i have done so far)
