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

def isMarketOpen() -> bool:
    """
    Checks if the market is open

    Returns: True if the market is open, False otherwise
    """
    isOpen = supabase.table("market_State").select("state").order("id", desc=True).limit(1).execute().data
    return isOpen


def fetchProfile(userID: str) -> dict:
    """
    Fetches user data from profiles table using userId

    Args:
        userID (str): The ID of the user

    Returns: profile dictionary
    """

    return supabase.table("profiles").select("*").eq("userId", userID).execute().data[0]


def fetchPortfolio(userID: str, stockID: int) -> dict:
    """
    Fetches stock data from Portfolio table using userID and stockID

    Args:
        userID (str): The ID of the user
        sotckID (int): The ID of the stock

    Returns: Dictionary describing a user's holding of a stock
    """
    portfolios = supabase.table("Portfolio").select("*").match({"userId": userID, "stockId": stockID}).execute().data
    if portfolios:
        return portfolios[0]
    else:
        stock = supabase.table("stock_price").select("stock_price").eq("stockId", stockID).execute().data
        portfolio = supabase.table("Portfolio").select("Portfolio_ID").eq("userId", userID).order("Portfolio_ID", desc=True).limit(1).execute().data
        if not stock:
            stock = [{"stock_price": 0}]
        if not portfolio:
            portfolio = [{"Portfolio_ID": 0}]

        stock = stock[0]
        portfolio = portfolio[0]
        return {"stockId": stockID, "quantity": 0, "userId": userID, "Price": stock["stock_price"], "Portfolio_ID": portfolio["Portfolio_ID"]+1}


def exchangeStock(buyerProfile: dict, buyerPortfolio: dict, sellerProfile: dict, sellerPortfolio: dict, stockPrice: float) -> None:
    """
    Updates buyer and seller profiles & portfolios when a stock is transacted

    Args:
        buyerProfile (dict): The buyer's profile data, includes balance and net worth
        buyerPortfolio (dict): Data related to the buyer's holdings of a certain stock
        sellerProfile (dict): The seller's profile data, includes balance and net worth
        sellerPortfolio (dict): Data related to the seller's holdings of a certain stock
        stockPrice (float): The curent sell price of the transacted stock

    Returns: None
    """
    buyerPortfolio["quantity"] += 1
    supabase.table("Portfolio").upsert(buyerPortfolio)
    supabase.table("profiles").update({"balance": buyerProfile["balance"]-stockPrice}).eq("userId", buyerProfile["userId"])

    sellerPortfolio["quantity"] -= 1
    supabase.table("Portfolio").upsert(sellerPortfolio)
    supabase.table("profiles").update({"balance": sellerProfile["balance"] + stockPrice}).eq("userId", sellerProfile["userId"])


def logTransaction(buyInfo: dict, sellInfo: dict) -> None:
    """
    Logs buy and sell tansaction info in the inactive_buy_sell

    Args:
        buyInfo (dict): Data related to the buy side of the transaction
        sellInfo (dict): Data relatedto the sell side of the transaction

    Returns: None
    """
    latestRow = supabase.table("inactive_buy_sell").select("id").order("id", desc=True).limit(1).execute().data
    latestId = latestRow[0]["id"]

    latestId += 1
    supabase.table("inactive_buy_sell").insert({"id": latestId,
                                                "delisted_time": datetime.now().isoformat(),
                                                "userId": buyInfo["buyerId"],
                                                "buy_or_sell": buyInfo["buy_or_sell"],
                                                "time_posted": buyInfo["time_posted"],
                                                "price": buyInfo["price"],
                                                "expirey": buyInfo["expirey"],
                                                "quantity": buyInfo["quantity"],
                                                "completed": True,
                                                "stockId": buyInfo["stockId"]
                                                }
                                               ).execute()

    latestId += 1
    supabase.table("inactive_buy_sell").insert({"id": latestId,
                                                "delisted_time": datetime.now().isoformat(),
                                                "userId": sellInfo["sellerId"],
                                                "buy_or_sell": sellInfo["buy_or_sell"],
                                                "time_posted": sellInfo["time_posted"],
                                                "price": sellInfo["price"],
                                                "expirey": sellInfo["expirey"],
                                                "quantity": sellInfo["quantity"],
                                                "completed": True,
                                                "stockId": sellInfo["stockId"]
                                                }
                                               ).execute()


def logUnfulfilledBuy(buyInfo: dict) -> None:
    """
    Logs info of a buy order if it cannot be fulfilled

    Args:
        buyInfo (dict): Data related to the buy side of a transaction

    Returns: None
    """
    latestRow = supabase.table("active_buy_sell").select("id").order("id", desc=True).limit(1).execute().data
    latestId = latestRow[0]["id"]

    latestId += 1
    supabase.table("active_buy_sell").insert({"id": latestId,
                                              "time_posted": buyInfo["time_posted"],
                                              "buy_or_sell": buyInfo["buy_or_sell"],
                                              "price": buyInfo["price"],
                                              "expirey": buyInfo["expirey"],
                                              "qunatity": buyInfo["qunatity"],
                                              "stockId": buyInfo["stockId"],
                                              "userId": buyInfo["userId"]
                                              }
                                             ).execute()


def update_entry():
    pass
