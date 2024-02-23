import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from APIFiles import testData
from APIFiles import supabaseMiddleman


app=FastAPI()
load_dotenv()

url = os.getenv('PUBLIC_SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)


async def buyMethod():
    # Return state by looking for the one with the biggest ID
    isOpen = supabaseMiddleman.isMarketOpen()
    if isOpen:
        buyInfo = {"userId": "572a902e-de7a-4739-adfe-f4af32a3f18b",
                   "buy_or_sell": True,
                   "stockId": 2,
                   "price": 15,
                   "quantity": 1,
                   "time_posted": datetime.now().isoformat(),
                   "expirey": (datetime.now() + timedelta(hours=1)).isoformat()  # This is a test value; users will input an expiry date
                   }
        # If the market is open, get all active sells for the stock <= buy_price, ordered by price
        print("pre call 1")

        validSells = supabase.table('active_buy_sell').select("*").match({'buy_or_sell': False, 'stockId': buyInfo["stockId"]}).lte('price', buyInfo["price"]).order('price').execute().data
        if validSells:
            cheapestSale = validSells[0]
            saleId = cheapestSale["Id"]
            sellInfo = {"userId": cheapestSale["userId"],
                        "buy_or_sell": False,
                        "stockId": cheapestSale["stockId"],
                        "price": cheapestSale["price"],
                        "quantity": 1,
                        "time_posted": cheapestSale["time_posted"],
                        "expirey": cheapestSale["expirey"]
                        }
            # Get Buyer and Seller user info and their holdings of the stock being traded
            buyerProfile = supabaseMiddleman.fetchProfile(buyInfo["userId"])
            buyerPortfolio = supabaseMiddleman.fetchPortfolio(buyInfo["userId"], buyInfo["stockId"])
            sellerProfile = supabaseMiddleman.fetchProfile(sellInfo["userId"])
            sellerPortfolio = supabaseMiddleman.fetchPortfolio(sellInfo["userId"], sellInfo["stockId"])
            return "Transaction profiles and portfolios fetched"

            # Exchange the stock by altering balances and stock holdings of buyer & seller (disabled for testing)
            # supabaseMiddleman.exchangeStock(buyerProfile, buyerPortfolio, sellerProfile, sellerPortfolio, sell_price)

            # Log the transactions by inserting them into the inactive_buy_sell table
            # supabaseMiddleman.logTransaction(buyInfo, sellInfo)

            # Delete active sell order that was just fufilled (disabled for testing)
            # supabase.table("active_buy_sell").delete().eq("id",saleId)
        else:
            # Insert the buy order into active_buy_sell if it can't be fufilled
            # supabaseMiddleman.logUnfulfilledBuy(buyInfo)
            return "No valid sale for this transaction"
        #     if insertInactive.error:
        #         raise HTTPException(status_code = 400, detail= f"Error inserting into inactive_buy_sell: {insertInactive}")
    else:
        # If the market is closed
        return "The market is closed"
