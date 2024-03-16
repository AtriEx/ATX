"""Supabase middleman should contain all of the database 
interactions in high-level generic functions."""

import os
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv

# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root
from supabase import Client, create_client
from util.date_extensions import from_supabase_date, to_supabase_date

load_dotenv("env/.env")
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def fetch_entries():
    """
    Fetches all entries from a table
    """


# needs a lot more checks and error handling
def insert_entry(table_name: str, entry: dict) -> None:
    """
    Inserts an entry into a table

    Args:
        table_name (str): The name of the table
        entry (dict): The entry to be inserted

    Returns: None
    """
    supabase.table(table_name).insert(entry).execute()


def is_market_open() -> bool:
    """
    Checks if the market is open

    Returns: True if the market is open, False otherwise
    """
    is_open = (
        supabase.table("market_State")
        .select("state")
        .order("id", desc=True)
        .limit(1)
        .execute()
        .data
    )
    return is_open


def fetch_profile(user_id: str) -> dict:
    """
    Fetches user data from profiles table using userId

    Args:
        user_id (str): The ID of the user

    Returns: profile dictionary
    """

    return (
        supabase.table("profiles").select("*").eq("userId", user_id).execute().data[0]
    )


# unreviewed
def fetch_portfolio(user_id: str, stock_id: int) -> dict:
    """
    Fetches stock data from portfolio table using userID and stockID

    Args:
        user_id (str): The ID of the user
        stock_id (int): The ID of the stock

    Returns: Dictionary describing a user's holding of a stock
    """
    portfolios = (
        supabase.table("portfolio")
        .select("*")
        .match({"userId": user_id, "stockId": stock_id})
        .execute()
        .data
    )
    if portfolios:
        return portfolios[0]

    stock = (
        supabase.table("stock_price")
        .select("stock_price")
        .eq("stockId", stock_id)
        .execute()
        .data
    )
    portfolio = (
        supabase.table("portfolio")
        .select("portfolio_ID")
        .eq("userId", user_id)
        .order("portfolio_ID", desc=True)
        .limit(1)
        .execute()
        .data
    )
    if not stock:
        stock = [{"stock_price": 0}]
    if not portfolio:
        portfolio = [{"portfolio_ID": 0}]

    stock = stock[0]
    portfolio = portfolio[0]
    return {
        "stockId": stock_id,
        "quantity": 0,
        "userId": user_id,
        "Price": stock["stock_price"],
        "portfolio_ID": portfolio["portfolio_ID"] + 1,
    }


# unreviewed
def exchange_stock(
    buyer_profile: dict,
    buyer_portfolio: dict,
    seller_profile: dict,
    seller_portfolio: dict,
    stock_price: float,
) -> None:
    """
    Updates buyer and seller profiles & portfolios when a stock is transacted

    Args:
        buyer_profile (dict): The buyer's profile data, includes balance and net worth
        buyer_portfolio (dict): Data related to the buyer's holdings of a certain stock
        seller_profile (dict): The seller's profile data, includes balance and net worth
        seller_portfolio (dict): Data related to the seller's holdings of a certain stock
        stock_price (float): The curent sell price of the transacted stock

    Returns: None
    """
    buyer_portfolio["quantity"] += 1
    supabase.table("portfolio").upsert(buyer_portfolio)
    supabase.table("profiles").update(
        {"balance": buyer_profile["balance"] - stock_price}
    ).eq("userId", buyer_profile["userId"])

    seller_portfolio["quantity"] -= 1
    supabase.table("portfolio").upsert(seller_portfolio)
    supabase.table("profiles").update(
        {"balance": seller_profile["balance"] + stock_price}
    ).eq("userId", seller_profile["userId"])


# unreviewed
def log_transaction(buy_info: dict, sell_info: dict) -> None:
    """
    Logs buy and sell tansaction info in the inactive_buy_sell

    Args:
        buy_info (dict): Data related to the buy side of the transaction
        sell_info (dict): Data relatedto the sell side of the transaction

    Returns: None
    """
    latest_row = (
        supabase.table("inactive_buy_sell")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
        .data
    )
    latest_id = latest_row[0]["id"]

    latest_id += 1
    supabase.table("inactive_buy_sell").insert(
        {
            "id": latest_id,
            "delisted_time": datetime.now().isoformat(),
            "userId": buy_info["buyerId"],
            "buy_or_sell": buy_info["buy_or_sell"],
            "time_posted": buy_info["time_posted"],
            "price": buy_info["price"],
            "expirey": buy_info["expirey"],
            "quantity": buy_info["quantity"],
            "completed": True,
            "stockId": buy_info["stockId"],
        }
    ).execute()

    latest_id += 1
    supabase.table("inactive_buy_sell").insert(
        {
            "id": latest_id,
            "delisted_time": datetime.now().isoformat(),
            "userId": sell_info["sellerId"],
            "buy_or_sell": sell_info["buy_or_sell"],
            "time_posted": sell_info["time_posted"],
            "price": sell_info["price"],
            "expirey": sell_info["expirey"],
            "quantity": sell_info["quantity"],
            "completed": True,
            "stockId": sell_info["stockId"],
        }
    ).execute()


# unreviewed
def log_unfulfilled_buy(buy_info: dict) -> None:
    """
    Logs info of a buy order if it cannot be fulfilled

    Args:
        buy_info (dict): Data related to the buy side of a transaction

    Returns: None
    """
    latest_row = (
        supabase.table("active_buy_sell")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
        .data
    )
    latest_id = latest_row[0]["id"]

    latest_id += 1
    supabase.table("active_buy_sell").insert(
        {
            "id": latest_id,
            "time_posted": buy_info["time_posted"],
            "buy_or_sell": buy_info["buy_or_sell"],
            "price": buy_info["price"],
            "expirey": buy_info["expirey"],
            "qunatity": buy_info["qunatity"],
            "stockId": buy_info["stockId"],
            "userId": buy_info["userId"],
        }
    ).execute()


def update_entry():
    """
    Updates an entry in a table
    """


def migrate_price_changes(hour: datetime):

    current_hour_time = hour.replace(minute=0, second=0, microsecond=0)
    last_hour_time = current_hour_time - timedelta(hours=1)
    two_hours_ago = current_hour_time - timedelta(hours=2)
    last_day_time = current_hour_time - timedelta(days=1)

    all_stock_ids = supabase.table("stock_info").select("id").execute().data
    all_hourly_price_changes = (
        supabase.table("stock_price_history_daily") 
        .select("changed_at, price, stockId") 
        .order("changed_at")
        .order("stockId")
        .gte("changed_at", to_supabase_date(last_hour_time))
        .lt("changed_at", to_supabase_date(current_hour_time))
        .execute().data
    )
    all_hourly_fulfilled = (supabase
        .table("inactive_buy_sell")
        .select("quantity, stockId")
        .gte("delisted_time", to_supabase_date(last_hour_time))
        .lt("delisted_time", to_supabase_date(current_hour_time))
        .eq("completed", "TRUE")
        .eq("buy_or_sell", "TRUE")
        .order("stockId")
        .execute().data
    )

    last_weekly_history = (
        supabase.table("stock_price_history_weekly")
        .select("closing_price", "stockId")
        .eq("starting_hour", to_supabase_date(two_hours_ago))
        .execute().data
    )
    
    hourly_volume_table = {}
    hourly_change_table = {}

    for stock_id in all_stock_ids:
        hourly_volume_table[stock_id["id"]] = (0, 0)
        hourly_change_table[stock_id["id"]] = {
            "starting_hour": to_supabase_date(last_hour_time),
            "stockId": stock_id["id"],
            "average_price": 0,
            "highest_price": 0,
            "lowest_price": 0,
            "opening_price": 0,
            "closing_price": 0,
            "volume_of_sales": 0,
        }

    for weekly_entry in last_weekly_history:
        hourly_change_table[weekly_entry["stockId"]]["opening_price"] = weekly_entry["closing_price"]
        hourly_change_table[weekly_entry["stockId"]]["closing_price"] = weekly_entry["closing_price"]
        hourly_change_table[weekly_entry["stockId"]]["highest_price"] = weekly_entry["closing_price"]
        hourly_change_table[weekly_entry["stockId"]]["lowest_price"] = weekly_entry["closing_price"]
        hourly_change_table[weekly_entry["stockId"]]["average_price"] = weekly_entry["closing_price"]

    for fulfilled_order in all_hourly_fulfilled:
        hourly_volume_table[fulfilled_order["stockId"]] += (fulfilled_order["quantity"], fulfilled_order["quantity"] * fulfilled_order["price"])

    print(hourly_volume_table)

    current_stock = all_hourly_price_changes[0]["stockId"]
    hourly_highest = all_hourly_price_changes[0]["price"] 
    hourly_lowest = all_hourly_price_changes[0]["price"] 
    hourly_last_price = all_hourly_price_changes[0]["price"] 

    for price_change in all_hourly_price_changes:
        if price_change["stockId"] != current_stock:
            hourly_change_table[current_stock]["average_price"] = (
                hourly_last_price if hourly_volume_table[current_stock][0] == 0
                else hourly_volume_table[current_stock][1] / hourly_volume_table[current_stock][0]
            )
            hourly_change_table[current_stock]["highest_price"] = hourly_highest
            hourly_change_table[current_stock]["lowest_price"] = hourly_lowest
            hourly_change_table[current_stock]["closing_price"] = hourly_last_price
            hourly_change_table[current_stock]["volume_of_sales"] = hourly_volume_table[current_stock][0]

            current_stock = price_change["stockId"]
            hourly_highest = price_change["price"]
            hourly_lowest = price_change["price"]
            hourly_last_price = price_change["price"]
        else:
            hourly_highest = max(hourly_highest, price_change["price"])
            hourly_lowest = min(hourly_lowest, price_change["price"])
            hourly_last_price = price_change["price"]
    

    hourly_change_table[current_stock]["average_price"] = (
        hourly_last_price if hourly_volume_table[current_stock][0] == 0
        else hourly_volume_table[current_stock][1] / hourly_volume_table[current_stock][0]
    )
    hourly_change_table[current_stock]["highest_price"] = hourly_highest
    hourly_change_table[current_stock]["lowest_price"] = hourly_lowest
    hourly_change_table[current_stock]["closing_price"] = hourly_last_price
    hourly_change_table[current_stock]["volume_of_sales"] = hourly_volume_table[current_stock][0]

    print("\nHourly Volume Table \n\n")
    print(hourly_volume_table)
    print("\nHourly Change Table \n\n")
    pprint(hourly_change_table[1])
    print("\n\n")
    pprint(all_hourly_price_changes)


    supabase.table("stock_price_history_weekly").insert(list(hourly_change_table.values())).execute();

    # If hour == 0 we're at the end of the day
    if current_hour_time.hour == 0:
    
        monthly_entries = []
        todays_weekly_entries = (
            supabase.table("stock_price_history_weekly")
            .select("opening_price", "closing_price", "stockId", "average_price", "volume_of_sales", "lowest_price", "highest_price")
            .gte("starting_hour", to_supabase_date(last_day_time))
            .lt("starting_hour", to_supabase_date(current_hour_time))
            .order("starting_hour")
            .order("stockId")
            .execute().data
        )

        # We do a little grouping
        weekly_group_table = {
        }

        for weekly_entry in todays_weekly_entries:
            if weekly_entry["stockId"] not in weekly_group_table:
                weekly_group_table[weekly_entry["stockId"]] = [weekly_entry]
            else:
                weekly_group_table[weekly_entry["stockId"]] += [weekly_entry]

        for stock_group in list(weekly_group_table.values()):
            current_stock_id = stock_group[0]["stockId"]
            open_price = stock_group[0]["opening_price"]
            highest_price = stock_group[0]["highest_price"]
            lowest_price = stock_group[0]["lowest_price"]
            closing_price = stock_group[len(stock_group)]["closing_price"]
            total_volume = 0
            total_price_sum = 0

            for weekly_entry in stock_group:
                total_volume += weekly_entry["volume_of_sales"]
                total_price_sum += weekly_entry["average_price"] * weekly_entry["volume_of_sales"]

                highest_price = max(highest_price, weekly_entry["highest_price"])
                lowets_price = min(lowest_price, weekly_entry["lowest_price"])
            
            monthly_entries += [{
                "starting_hour": current_hour_time,
                "stockId": current_stock_id, 
                "opening_price": open_price,
                "closing_price": closing_price,
                "highest_price": highest_price,
                "lowest_price": lowest_price,
                "volume_of_sales": total_volume,
                "average_price": total_price_sum / total_volume
            }]

        supabase.table("stock_price_history_monthly").insert(monthly_entries).execute
