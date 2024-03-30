"""API handler for giving daily bonus to users"""

import os
import random

from dotenv import load_dotenv

from supabase import Client, create_client

load_dotenv()

url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_random_stock():
    stock_ids = supabase.table("stock_info").select("id").execute()
    if stock_ids.data:
        random_id = random.choice(stock_ids.data)['id']
        random_stock = supabase.table("stock_info").select("*").eq('id', random_id).execute()
        return random_stock.data[0] if random_stock.data else None
    return None


def add_stock_to_portfolio(user_id, stock_id):
    response = supabase.table("portfolio").insert({
        "userId": user_id,
        "stockId": stock_id,
        "quantity": 1,
        "price_avg": 0  # Assuming the stock is given for free as a bonus
    }).execute()
    return response


def give_daily_bonus(user_id):
    return "Daily Bonus Given"
