import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from util.ext import test_data
from database.supabase.store import supabase_middleman
from uuid import uuid4

app = FastAPI()
load_dotenv()


#
def create_buy_order():
    # Insert a test entry into the active_buy_sell table
    test_entry = test_data.test_entry_1()
    supabase_middleman.insert_entry("active_buy_sell", test_entry)
    return


def create_sell_order():
    # Insert a test entry into the active_buy_sell table
    test_entry = test_data.test_entry_2()
    supabase_middleman.insert_entry("active_buy_sell", test_entry)
    return


"""
active_buy_sell table schema:
time_posted: timestamp
buy_or_sell: bool
price: int8
expirey: timestamp
quantity: int (this should always be 1. when we have an order submitted for 10, we break it up into 10 identical rows of quant 1)
stockId: int8
userId: uuid(str)
orderId: uuid(str)
"""


# Creates entries to active_buy_sell table, adding one entry for each quantity
def create_active_order(
    time_posted: datetime,
    buy_or_sell: bool,
    price: int,
    expirey: datetime,
    quantity: int,
    stock_id: int,
    user_id: str,
):
    generated_order_id = str(uuid4())

    if buy_or_sell:
        supabase_middleman.escrow_funds(user_id, price, quantity)
    else:
        supabase_middleman.escrow_stock(user_id, stock_id, quantity)

    # Generate an entry for each quantity and insert those entries into the table
    for i in range(quantity):
        entry = {
            "time_posted": time_posted,
            "buy_or_sell": buy_or_sell,
            "price": price,
            "expirey": expirey,
            "quantity": 1,
            "stockId": stock_id,
            "userId": user_id,
            "orderId": generated_order_id,
            "has_been_processed": False,
        }
        # Insert the entry into the active_buy_sell table
        supabase_middleman.insert_entry("active_buy_sell", entry)
    return
