import os
import traceback

from datetime import timedelta, datetime
from dotenv import load_dotenv
from database import supabase_middleman
import random

from supabase import Client, create_client

load_dotenv("env/.env")
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def test_migrate_history_middle_day():
    print("test", flush=True)
    current_hour_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    last_hour_time = current_hour_time - timedelta(hours=1)
    for delta_t in range(1,20):
        supabase_middleman.insert_entry("stock_price_history_daily", {
            "changed_at": (current_hour_time - timedelta(minutes=delta_t)).strftime("%Y-%m-%d %H:%M:%S"),
            "price": random.randint(1,100),
            "stockId": 1,
        })
    try:
        supabase_middleman.migrate_price_changes()

    except:
        print("\n\nmigrate_price_changes failed\n")
        print(traceback.format_exc())
    (
        supabase.table("stock_price_history_daily")
        .delete()
        .gt("changed_at", last_hour_time.strftime("%Y-%m-%d %H:%M:%S"))
        .lt("changed_at", current_hour_time.strftime("%Y-%m-%d %H:%M:%S"))
        .execute()
    )

def test_migrate_history_end_of_day():
    current_hour_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    last_hour_time = current_hour_time - timedelta(hours=1)
    for delta_t in range(1,20):
        supabase_middleman.insert_entry("stock_price_history_daily", {
            "changed_at": (current_hour_time - timedelta(minutes=delta_t)).strftime("%Y-%m-%d %H:%M:%S"),
            "price": random.randint(1,100),
            "stockId": 1,
        })
    supabase_middleman.migrate_price_changes()


