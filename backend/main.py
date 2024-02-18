# from routers import items, users
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI

# pylint: disable=no-name-in-module
from supabase import Client, create_client

from backend import supabaseMiddleman

app = FastAPI()
load_dotenv()

url = "https://wxskoymvdulyscwhebze.supabase.co"
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# @app.get('quick_buy')
@app.get("/")
async def quickBuy():
    """
    This endpoint places a buy order for exactly one share of a stock
    and tries to execute it if the market is open
    """
    # Return state by looking for the one with the biggest ID
    isOpen = (
        supabase.table("market_State")
        .select("state")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )
    if not isOpen:
        return "The market is closed"

    buyInfo = {
        "buyerId": "572a902e-de7a-4739-adfe-f4af32a3f18b",
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
    validSells = (
        supabase.table("active_buy_sell")
        .select("*")
        .match({"buy_or_sell": False, "stockId": buyInfo["stockId"]})
        .lte("price", buyInfo["price"])
        .order("price")
        .execute()
        .data
    )

    if not validSells:
        # Insert the buy order into active_buy_sell if it can't be fufilled
        # supabaseMiddleman.logUnfulfilledBuy(buyInfo)
        return "No valid sale for this transaction"
        # if insertInactive.error:
        #     raise HTTPException(
        #         status_code=400,
        #         detail=f"Error inserting into inactive_buy_sell: {insertInactive}",
        #     )

    cheapestSale = validSells[-1]
    saleId = cheapestSale["id"]
    sellInfo = {
        "sellerId": cheapestSale["userId"],
        "buy_or_sell": False,
        "stockId": cheapestSale["stockId"],
        "price": cheapestSale["price"],
        "quantity": 1,
        "time_posted": cheapestSale["time_posted"],
        "expirey": cheapestSale["expirey"],
    }

    # Get Buyer and Seller user info and their holdings of the stock being traded
    buyerProfile = supabaseMiddleman.fetchProfile(buyInfo["buyerId"])
    buyerPortfolio = supabaseMiddleman.fetchPortfolio(
        buyInfo["buyerId"], buyInfo["stockId"]
    )
    sellerProfile = supabaseMiddleman.fetchProfile(sellInfo["sellerId"])
    sellerPortfolio = supabaseMiddleman.fetchPortfolio(
        sellInfo["sellerId"], sellInfo["stockId"]
    )

    print("Transaction profiles and portfolios fetched")

    # Exchange the stock by altering balances and stock holdings of buyer & seller
    # (disabled for testing)
    # supabaseMiddleman.exchangeStock(
    #     buyerProfile, buyerPortfolio, sellerProfile, sellerPortfolio, sell_price
    # )

    # Log the transactions by inserting them into the inactive_buy_sell table
    # supabaseMiddleman.logTransaction(buyInfo, sellInfo)

    # Delete active sell order that was just fufilled (disabled for testing)
    # supabase.table("active_buy_sell").delete().eq("id",saleId)


# my_list = [datetime.now(), False, 20, None, 1, 1, '36d22a68-ca25-4110-b769-44cf5b4a1c89']

# app.include_router(users.router)
# app.include_router(items.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
