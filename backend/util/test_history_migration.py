import os
import traceback

from datetime import timedelta, datetime
from dotenv import load_dotenv
from database import supabase_middleman
from util.date_extensions import from_supabase_date, to_supabase_date
import random

from supabase import Client, create_client

load_dotenv("env/.env")
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def test_migrate_history_middle_day(clean):

    default_opening_price = 300

    # Create test data
    test_hour_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    last_hour_time = test_hour_time - timedelta(hours=1)
    two_hours_before = test_hour_time - timedelta(hours=2)
    for delta_t in range(1,20):
        supabase_middleman.insert_entry("stock_price_history_daily", {
            "changed_at": to_supabase_date(test_hour_time - timedelta(minutes=delta_t)),
            "price": random.randint(1,100),
            "stockId": 1,
        })

    all_stock_ids = supabase.table("stock_info").select("id").execute().data

    for stock_id in all_stock_ids:
        supabase_middleman.insert_entry("stock_price_history_weekly", {
                "stockId": stock_id["id"],
                "starting_hour": to_supabase_date(two_hours_before),
                "average_price": 200,
                "highest_price": 400,
                "lowest_price":50,
                "opening_price": 100,
                "closing_price": default_opening_price ,
                "volume_of_sales": 2000,
            })

    # Run test
    try:
        supabase_middleman.migrate_price_changes(test_hour_time)

    except:
        print("\n\nmigrate_price_changes failed\n")
        print(traceback.format_exc())

    # TODO: Validate test data
    new_weekly_entries = (
        supabase.table("stock_price_history_weekly")
        .select("stockId", "average_price", "highest_price", "opening_price", "closing_price", "volume_of_sales")
        .eq("starting_hour", to_supabase_date(last_hour_time))
        .execute().data
    )

    opening_pass_value = False
    for weekly_entry in new_weekly_entries:
        opening_pass_value = opening_pass_value or (weekly_entry["opening_price"] == default_opening_price)

    print(f"OPENING VALUE TEST: {"PASS" if opening_pass_value else "FAIL"}")

    if clean:
        # Clean up test data
        (
            supabase.table("stock_price_history_daily")
            .delete()
            .gt("changed_at", to_supabase_date(last_hour_time))
            .lt("changed_at", to_supabase_date(test_hour_time))
            .execute()
        )
        (
            supabase.table("stock_price_history_weekly")
            .delete()
            .eq("starting_hour", to_supabase_date(two_hours_before))
            .execute()
        )
        (
            supabase.table("stock_price_history_weekly")
            .delete()
            .eq("starting_hour", to_supabase_date(last_hour_time))
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


