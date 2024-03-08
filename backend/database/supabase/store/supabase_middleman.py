import os
from dotenv import load_dotenv
from typing import Literal
from datetime import datetime
from supabase import create_client, Client

load_dotenv("env/.env")
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def fetch_entries():
    pass


# needs a lot more checks and error handling
def insert_entry(tableName: str, entry: dict) -> None:
    supabase.table(tableName).insert(entry).execute()
    return


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


def fetch_profile(userID: str) -> dict:
    """
    Fetches user data from profiles table using userId

    Args:
        userID (str): The ID of the user

    Returns: profile dictionary
    """

    return supabase.table("profiles").select("*").eq("userId", userID).execute().data[0]


# unreviewed
def fetch_portfolio(userID: str, stockID: int) -> dict:
    """
    Fetches stock data from portfolio table using userID and stockID

    Args:
        userID (str): The ID of the user
        sotckID (int): The ID of the stock

    Returns: Dictionary describing a user's holding of a stock
    """
    portfolios = (
        supabase.table("portfolio")
        .select("*")
        .match({"userId": userID, "stockId": stockID})
        .execute()
        .data
    )
    if portfolios:
        return portfolios[0]
    else:
        stock = (
            supabase.table("stock_price")
            .select("stock_price")
            .eq("stockId", stockID)
            .execute()
            .data
        )
        portfolio = (
            supabase.table("portfolio")
            .select("portfolio_ID")
            .eq("userId", userID)
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
            "stockId": stockID,
            "quantity": 0,
            "userId": userID,
            "Price": stock["stock_price"],
            "portfolio_ID": portfolio["portfolio_ID"] + 1,
        }


# unreviewed
def exchange_stock(
    buyer_profile: dict,
    buyer_portfolio: dict,
    seller_profile: dict,
    seller_portfolio: dict,
    stockPrice: float,
) -> None:
    """
    Updates buyer and seller profiles & portfolios when a stock is transacted

    Args:
        buyer_profile (dict): The buyer's profile data, includes balance and net worth
        buyer_portfolio (dict): Data related to the buyer's holdings of a certain stock
        seller_profile (dict): The seller's profile data, includes balance and net worth
        seller_portfolio (dict): Data related to the seller's holdings of a certain stock
        stockPrice (float): The curent sell price of the transacted stock

    Returns: None
    """
    buyer_portfolio["quantity"] += 1
    supabase.table("portfolio").upsert(buyer_portfolio)
    supabase.table("profiles").update(
        {"balance": buyer_profile["balance"] - stockPrice}
    ).eq("userId", buyer_profile["userId"])

    seller_portfolio["quantity"] -= 1
    supabase.table("portfolio").upsert(seller_portfolio)
    supabase.table("profiles").update(
        {"balance": seller_profile["balance"] + stockPrice}
    ).eq("userId", seller_profile["userId"])


# unreviewed
def log_transaction(buyInfo: dict, sellInfo: dict) -> None:
    """
    Logs buy and sell tansaction info in the inactive_buy_sell

    Args:
        buyInfo (dict): Data related to the buy side of the transaction
        sellInfo (dict): Data relatedto the sell side of the transaction

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
    latestId = latest_row[0]["id"]

    latestId += 1
    supabase.table("inactive_buy_sell").insert(
        {
            "id": latestId,
            "delisted_time": datetime.now().isoformat(),
            "userId": buyInfo["buyerId"],
            "buy_or_sell": buyInfo["buy_or_sell"],
            "time_posted": buyInfo["time_posted"],
            "price": buyInfo["price"],
            "expirey": buyInfo["expirey"],
            "quantity": buyInfo["quantity"],
            "completed": True,
            "stockId": buyInfo["stockId"],
        }
    ).execute()

    latestId += 1
    supabase.table("inactive_buy_sell").insert(
        {
            "id": latestId,
            "delisted_time": datetime.now().isoformat(),
            "userId": sellInfo["sellerId"],
            "buy_or_sell": sellInfo["buy_or_sell"],
            "time_posted": sellInfo["time_posted"],
            "price": sellInfo["price"],
            "expirey": sellInfo["expirey"],
            "quantity": sellInfo["quantity"],
            "completed": True,
            "stockId": sellInfo["stockId"],
        }
    ).execute()


# unreviewed
def log_unfulfilled_buy(buyInfo: dict) -> None:
    """
    Logs info of a buy order if it cannot be fulfilled

    Args:
        buyInfo (dict): Data related to the buy side of a transaction

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
    latestId = latest_row[0]["id"]

    latestId += 1
    supabase.table("active_buy_sell").insert(
        {
            "id": latestId,
            "time_posted": buyInfo["time_posted"],
            "buy_or_sell": buyInfo["buy_or_sell"],
            "price": buyInfo["price"],
            "expirey": buyInfo["expirey"],
            "qunatity": buyInfo["qunatity"],
            "stockId": buyInfo["stockId"],
            "userId": buyInfo["userId"],
        }
    ).execute()


def update_entry():
    pass


def escrow_funds(user_id, price, quantity) -> None:
    """
    Escrows funds for a buy order

    Args:
        userId (str): The ID of the user
        price (int): The price of the stock
        quantity (int): The quantity of the stock

    Returns: None
    """
    user_profile = fetch_profile(user_id)
    supabase.table("profiles").update(
        {"balance": user_profile["balance"] - price * quantity}
    ).eq("userId", user_id)


def escrow_stock(user_id, stock_id, quantity) -> None:
    """
    Escrows stock for a sell order

    Args:
        userId (str): The ID of the user
        stockId (int): The ID of the stock
        quantity (int): The quantity of the stock

    Returns: None
    """
    portfolio = fetch_portfolio(user_id, stock_id)
    supabase.table("portfolio").update(
        {"quantity": portfolio["quantity"] - quantity}
    ).eq("portfolio_ID", portfolio["portfolio_ID"])
