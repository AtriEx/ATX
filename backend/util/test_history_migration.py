import os
import traceback
import sys

from datetime import timedelta, datetime
from dotenv import load_dotenv
from database import supabase_middleman
from util.date_extensions import to_supabase_date
import random

from supabase import Client, create_client

load_dotenv("env/.env")
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key) # type: ignore

def test_migrate_history_middle_day(test_time: datetime, clean: bool):
    """
    Tests middle of day migration of order history, creates test data and cleans it if requested.

    Args: 
        test_time (datetime): End of hour time, test data will be created between this and one hour before this.
        clean (bool): Specifies whether or not data is cleaned after testing
    """

    default_opening_price = 300

    # Create test data
    test_hour_time = test_time.replace(minute=0, second=0, microsecond=0)
    last_hour_time = test_hour_time - timedelta(hours=1)
    two_hours_before = test_hour_time - timedelta(hours=2)

    
    all_stock_ids = supabase.table("stock_info").select("id").execute().data

    test_daily_data = []
    valid_max_price = 0
    valid_min_price = sys.maxsize
    valid_close_price = 0
    for delta_t in range(1,20):
        price = random.randint(1,100)
        valid_max_price = max(valid_max_price, price)
        valid_min_price = min(valid_min_price, price)
        if delta_t == 1:
            valid_close_price = price
        test_daily_data += [{
            "changed_at": to_supabase_date(test_hour_time - timedelta(minutes=delta_t)),
            "price": price,
            "stockId": 1,
        }]

    supabase.table("stock_price_history_daily").insert(test_daily_data).execute()

    test_weekly_data = []
    for stock_id in all_stock_ids:
        test_weekly_data += [{
                "stockId": stock_id["id"],
                "starting_hour": to_supabase_date(two_hours_before),
                "average_price": 200,
                "highest_price": 400,
                "lowest_price":50,
                "opening_price": 100,
                "closing_price": default_opening_price ,
                "volume_of_sales": 2000,
        }]

    supabase.table("stock_price_history_weekly").insert(test_weekly_data).execute()

    # Run test
    try:
        supabase_middleman.migrate_price_changes(test_hour_time)
        new_weekly_entry = (
            supabase.table("stock_price_history_weekly")
            .select("stockId", "average_price", "highest_price", "opening_price", "lowest_price", "closing_price", "volume_of_sales")
            .eq("starting_hour", to_supabase_date(last_hour_time))
            .eq("stockId", 1)
            .limit(1)
            .single()
            .execute().data
        )

        opening_pass_value = (new_weekly_entry["opening_price"] == default_opening_price)
        closing_pass_value = (new_weekly_entry["closing_price"] == valid_close_price)
        highest_pass_value = (new_weekly_entry["highest_price"] == valid_max_price)
        lowest_pass_value = (new_weekly_entry["lowest_price"] == valid_min_price)

        print(f"OPENING VALUE TEST: {"PASS" if opening_pass_value else f"FAIL. Expected: {default_opening_price} - Actual:{new_weekly_entry["opening_price"]}"}")
        print(f"CLOSING VALUE TEST: {"PASS" if closing_pass_value else f"FAIL. Expected: {valid_close_price} - Actual:{new_weekly_entry["closing_price"]}"}")
        print(f"HIGHEST VALUE TEST: {"PASS" if highest_pass_value else f"FAIL. Expected: {valid_max_price} - Actual:{new_weekly_entry["highest_price"]}"}")
        print(f"LOWEST VALUE TEST: {"PASS" if lowest_pass_value else f"FAIL. Expected: {valid_min_price} - Actual:{new_weekly_entry["lowest_price"]}"}")
    except:
        print("migrate_price_changes failed")
        print(traceback.format_exc())


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

def test_migrate_history_end_of_day(test_time: datetime, clean: bool):
    """
    Tests end of day migration of order history, creates test data and cleans it if requested.

    Args: 
        test_time (datetime): End of day time, test data will be created between this and one day before this.
        clean (bool): Specifies whether or not data is cleaned after testing
    """
    default_opening_price = 300
     
    current_hour_time = test_time.replace(minute=0, second=0, microsecond=0, hour=0)
    last_day_time = current_hour_time - timedelta(days=1)

    all_stock_ids = supabase.table("stock_info").select("id").execute().data

    test_daily_data = []
    valid_max_price = 0
    valid_min_price = sys.maxsize
    valid_close_price = 0

    for delta_t_h in range(0, 24):
        for delta_t_m in range(1,20):
            temp_price = random.randint(1,100)
            valid_max_price = max(valid_max_price, temp_price)
            valid_min_price = min(valid_min_price, temp_price)
            if delta_t_h == 1 and delta_t_m == 1:
                valid_close_price = temp_price
            test_daily_data += [{
                "changed_at": (current_hour_time - timedelta(minutes=delta_t_m, hours=delta_t_h)).strftime("%Y-%m-%d %H:%M:%S"),
                "price": temp_price,
                "stockId": 1,
            }]

    supabase.table("stock_price_history_daily").insert(test_daily_data).execute()

    test_weekly_data = []
    for stock_id in all_stock_ids:
        test_weekly_data += [{
                "stockId": stock_id["id"],
                "starting_hour": to_supabase_date(current_hour_time - timedelta(hours=25)),
                "average_price": 200,
                "highest_price": 400,
                "lowest_price":50,
                "opening_price": 100,
                "closing_price": default_opening_price ,
                "volume_of_sales": 2000,
        }]

    supabase.table("stock_price_history_weekly").insert(test_weekly_data).execute()
    try:
        for delta_t_h in range(23, -1, -1):
            supabase_middleman.migrate_price_changes(current_hour_time - timedelta(hours=delta_t_h))

        new_monthly_entry = (
            supabase.table("stock_price_history_monthly")
            .select("stockId", "average_price", "highest_price", "opening_price", "lowest_price", "closing_price", "volume_of_sales")
            .eq("starting_hour", to_supabase_date(last_day_time))
            .eq("stockId", 1)
            .limit(1)
            .single()
            .execute().data
        )

        opening_pass_value = (new_monthly_entry["opening_price"] == default_opening_price)
        closing_pass_value = (new_monthly_entry["closing_price"] == valid_close_price)
        highest_pass_value = (new_monthly_entry["highest_price"] == valid_max_price)
        lowest_pass_value = (new_monthly_entry["lowest_price"] == valid_min_price)

        print(f"OPENING VALUE TEST: {"PASS" if opening_pass_value else f"FAIL. Expected: {default_opening_price} - Actual:{new_monthly_entry["opening_price"]}"}")
        print(f"CLOSING VALUE TEST: {"PASS" if closing_pass_value else f"FAIL. Expected: {valid_close_price} - Actual:{new_monthly_entry["closing_price"]}"}")
        print(f"HIGHEST VALUE TEST: {"PASS" if highest_pass_value else f"FAIL. Expected: {valid_max_price} - Actual:{new_monthly_entry["highest_price"]}"}")
        print(f"LOWEST VALUE TEST: {"PASS" if lowest_pass_value else f"FAIL. Expected: {valid_min_price} - Actual:{new_monthly_entry["lowest_price"]}"}")
    except:
        print("test_migrate_history_end_of_day failed")
        print(traceback.format_exc())

    if clean:
        (
            supabase.table("stock_price_history_daily")
            .delete()
            .gt("changed_at", to_supabase_date(last_day_time))
            .lt("changed_at", to_supabase_date(current_hour_time))
            .execute()
        )
        (
            supabase.table("stock_price_history_weekly")
            .delete()
            .gte("starting_hour", to_supabase_date(last_day_time - timedelta(hours=1)))
            .lt("starting_hour", to_supabase_date(current_hour_time))
            .execute()
        )
        (
            supabase.table("stock_price_history_monthly")
        )


