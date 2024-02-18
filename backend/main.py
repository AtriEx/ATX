#from routers import items, users
from datetime import datetime
from fastapi import FastAPI
from supabase import create_client, Client
import supabaseMiddleman

app = FastAPI()

url = "https://wxskoymvdulyscwhebze.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind4c2tveW12ZHVseXNjd2hlYnplIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNjY2NTAzMywiZXhwIjoyMDIyMjQxMDMzfQ.HaBk3QEcnHJaJ284RmHK49fMXmEPzTJHDvzwoQ-eRt0"
supabase: Client = create_client(url, key)

# Assuming someone has chosen to 'quick buy' a stock of quantity 1
# @app.get('quick_buy')
@app.get('/')
async def quick_buy():
    buyerID = "572a902e-de7a-4739-adfe-f4af32a3f18b"
    # Return state by looking for the one with the biggest ID
    isOpen = supabase.table('market_State').select('state').order('id', desc=True).limit(1).execute()
    if isOpen:
        
        # If the market is open
        active_buy_sell_entry = supabase.table('active_buy_sell').select("*").eq('buy_or_sell','TRUE').order('price', desc=True).execute().data
        
        # Check if 'buy_or_sell' is set to TRUE
        if active_buy_sell_entry:
            
            #return active_buy_sell_entry
            
            sellerID = active_buy_sell_entry[0]["userId"]
            active_buy_sell_entry[0].pop("id")
            
            buyerProfile = supabaseMiddleman.fetch_user_data(buyerID,"profiles")
            print("BuyerProfile Got")
            sellerProfile = supabaseMiddleman.fetch_user_data(sellerID,"profiles")
            print("SellerProfile Got")
            buyerPortfolio = supabaseMiddleman.fetch_user_data(buyerID,"Portfolio")
            print("BuyerPortfolio Got")
            sellerPortfolio = supabaseMiddleman.fetch_user_data(sellerID,"Portfolio")
            print("SellerPortfolio Got")
            
            supabase.table('inactive_buy_sell').insert(active_buy_sell_entry).execute()
            # Need to create a second entry from the buyers perspective
            
            print("Entry succesfully inserted")
            
            # Disabled for testing purposes
            #supabase.table('active_buy_sell').delete().match({'id':active_buy_sell_entry[0]['id']}).execute()
            print("Entry succesfully deleted")
            
            
            subtractFromBalance = {
                "balance": buyerProfile[0]["balance"] - active_buy_sell_entry[0]["price"] 
            }
            
            addToBalance = {
                "balance": sellerProfile[0]["balance"] + active_buy_sell_entry[0]["price"] 
            }
            # for stock in buyerPortfolio:
            #     if stock['stockID'] == 
            
            print("Checking if the user already has the stock")
            #return buyerPortfolio[0]
            if buyerPortfolio[0]["stockId"] == active_buy_sell_entry[0]["stockId"]:
                print ("User does have the stock")
                addToPortfolio = {
                "quantity": buyerPortfolio[0]["quantity"] + active_buy_sell_entry[0]["quantity"]
            }
                print("User did  have the stock, added more quantity to their portfolio") 
                
            else:
                newStockInsert = {'stockID': 123, 'userId': buyerID, 'quantity': 1, 'price':active_buy_sell_entry[0]['price']}
                supabase.table('portfolio').insert().execute()
                print("User did not have the stock, added a new entry to their portfolio") 
            
            supabase.table('profiles').update(addToBalance).eq("userId", buyerID).execute()
            
            return "User has succesfully bought the stock"
            
            
        #     if insertInactive.error:
        #         raise HTTPException(status_code = 400, detail= f"Error inserting into inactive_buy_sell: {insertInactive}")
        else:
            return "There is nothing in the active_buy_sell" 
    else:
        # If the market is closed
        return "The market is closed"
    
#my_list = [datetime.now(), False, 20, None, 1, 1, '36d22a68-ca25-4110-b769-44cf5b4a1c89']

# app.include_router(users.router)
# app.include_router(items.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}





