import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from util.ext import test_data
from database import supabase_middleman


app=FastAPI()
load_dotenv()

url = os.getenv('PUBLIC_SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)


def buy_order():
    # Return state by looking for the one with the biggest ID
    is_open = supabase_middleman.is_market_open()
    if is_open:
        buy_info = {"userId": "572a902e-de7a-4739-adfe-f4af32a3f18b",
                   "buy_or_sell": True,
                   "stockId": 2,
                   "price": 15,
                   "quantity": 1,
                   "time_posted": datetime.now().isoformat(),
                   "expirey": (datetime.now() + timedelta(hours=1)).isoformat()  # This is a test value; users will input an expiry date
                   }
        # If the market is open, get all active sells for the stock <= buy_price, ordered by price

        valid_sells = supabase.table('active_buy_sell').select("*").match({'buy_or_sell': False, 'stockId': buy_info["stockId"]}).lte('price', buy_info["price"]).order('price').execute().data
        if valid_sells:
            cheapest_sale = valid_sells[0]
            saleId = cheapest_sale["Id"]
            sell_info = {"userId": cheapest_sale["userId"],
                        "buy_or_sell": False,
                        "stockId": cheapest_sale["stockId"],
                        "price": cheapest_sale["price"],
                        "quantity": 1,
                        "time_posted": cheapest_sale["time_posted"],
                        "expirey": cheapest_sale["expirey"]
                        }
            # Get Buyer and Seller user info and their holdings of the stock being traded
            buyer_profile = supabase_middleman.fetch_profile(buy_info["userId"])
            buyer_portfolio = supabase_middleman.fetch_portfolio(buy_info["userId"], buy_info["stockId"])
            seller_profile = supabase_middleman.fetch_profile(sell_info["userId"])
            seller_portfolio = supabase_middleman.fetch_portfolio(sell_info["userId"], sell_info["stockId"])
            return "Transaction profiles and portfolios fetched"

            # Exchange the stock by altering balances and stock holdings of buyer & seller (disabled for testing)
            # supabaseMiddleman.exchange_stock(buyer_profile, buyer_portfolio, seller_profile, seller_portfolio, sell_price)

            # Log the transactions by inserting them into the inactive_buy_sell table
            # supabaseMiddleman.log_transaction(buy_info, sell_info)

            # Delete active sell order that was just fufilled (disabled for testing)
            # supabase.table("active_buy_sell").delete().eq("id",saleId)
        else:
            # Insert the buy order into active_buy_sell if it can't be fufilled
            # supabaseMiddleman.log_unfulfilled_buy(buy_info)
            return "No valid sale for this transaction"
        #     if insertInactive.error:
        #         raise HTTPException(status_code = 400, detail= f"Error inserting into inactive_buy_sell: {insertInactive}")
    else:
        # If the market is closed
        return "The market is closed"
