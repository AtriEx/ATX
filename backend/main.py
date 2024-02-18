"""Main API file for the backend."""

# from routers import items, users
from fastapi import FastAPI

# pylint: disable=no-name-in-module
from supabase import Client, create_client
from backend import supabaseMiddleman

APP = FastAPI()

URL = "https://wxskoymvdulyscwhebze.supabase.co"
# TODO: put in config?
# pylint: disable=line-too-long
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind4c2tveW12ZHVseXNjd2hlYnplIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNjY2NTAzMywiZXhwIjoyMDIyMjQxMDMzfQ.HaBk3QEcnHJaJ284RmHK49fMXmEPzTJHDvzwoQ-eRt0"
SUPABASE: Client = create_client(URL, KEY)


# @app.get('quick_buy')
@APP.get("/")
async def quickBuy():
    """
    Assuming someone has chosen to 'quick buy' a stock of quantity 1
    """

    buyerId = "572a902e-de7a-4739-adfe-f4af32a3f18b"
    # Return state by looking for the one with the biggest ID
    isOpen = (
        SUPABASE.table("market_State")
        .select("state")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )
    if not isOpen:
        # If the market is closed
        return "The market is closed"

    # If the market is open
    activeBuySellEntry = (
        SUPABASE.table("active_buy_sell")
        .select("*")
        .eq("buy_or_sell", "TRUE")
        .order("price", desc=True)
        .execute()
        .data
    )

    if not activeBuySellEntry:
        return "There is nothing in the active_buy_sell"

    # return active_buy_sell_entry

    sellerId = activeBuySellEntry[0]["userId"]
    activeBuySellEntry[0].pop("id")

    # FIXME: unused
    # buyer_profile = supabaseMiddleman.fetch_user_data(buyer_id, "profiles")
    print("BuyerProfile Got")
    sellerProfile = supabaseMiddleman.fetchUserData(sellerId, "profiles")
    print("SellerProfile Got")
    buyerPortfolio = supabaseMiddleman.fetchUserData(buyerId, "portfolio")
    print("BuyerPortfolio Got")
    # FIXME: unused
    # sellerPortfolio = supabaseMiddleman.fetch_user_data(seller_id,"portfolio")
    # print("SellerPortfolio Got")

    SUPABASE.table("inactive_buy_sell").insert(activeBuySellEntry).execute()
    # Need to create a second entry from the buyers perspective

    print("Entry succesfully inserted")

    # Disabled for testing purposes
    # supabase.table("active_buy_sell").delete().match(
    #     {"id": active_buy_sell_entry[0]["id"]}
    # ).execute()
    print("Entry succesfully deleted")

    # FIXME: unused
    # subtract_from_balance = {
    #     "balance": buyer_profile[0]["balance"] - active_buy_sell_entry[0]["price"]
    # }

    addToBalance = {
        "balance": sellerProfile[0]["balance"] + activeBuySellEntry[0]["price"]
    }
    # for stock in buyerPortfolio:
    #     if stock['stockID'] ==

    print("Checking if the user already has the stock")
    # return buyerPortfolio[0]
    if buyerPortfolio[0]["stockId"] == activeBuySellEntry[0]["stockId"]:
        print("User does have the stock")
        # FIXME: unused
        # add_to_portfolio = {
        #     "quantity": buyer_portfolio[0]["quantity"]
        #     + active_buy_sell_entry[0]["quantity"]
        # }
        print("User did  have the stock, added more quantity to their portfolio")

    else:
        newStockInsert = {
            "stockID": 123,
            "userId": buyerId,
            "quantity": 1,
            "price": activeBuySellEntry[0]["price"],
        }
        SUPABASE.table("portfolio").insert(newStockInsert).execute()
        print("User did not have the stock, added a new entry to their portfolio")

    SUPABASE.table("profiles").update(addToBalance).eq("userId", buyerId).execute()

    return "User has succesfully bought the stock"

    # if insertInactive.error:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"Error inserting into inactive_buy_sell: {insertInactive}",
    #     )


# my_list = [datetime.now(), False, 20, None, 1, 1, '36d22a68-ca25-4110-b769-44cf5b4a1c89']

# app.include_router(users.router)
# app.include_router(items.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
