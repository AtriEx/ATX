"""Supabase middleman should contain all of the database 
interactions in high-level generic functions."""

import os
import pprint
from datetime import datetime, timedelta

from dotenv import load_dotenv
from supabase import Client, create_client

from util.date_extensions import from_supabase_date, to_supabase_date

# pylint: disable=import-error,no-name-in-module # it's looking in the supabase folder in project root

load_dotenv(os.getenv("ENV_FILE", "env/.env"))
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)  # type: ignore


# needs a lot more checks and error handling
def insert_entry(table_name: str, entry: dict) -> None:
    """
    Inserts an entry into a table

    Args:
        table_name (str): The name of the table
        entry (dict): The entry to be inserted

    Returns: None
    """
    print(entry)
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
        .data.pop()
    )
    return is_open["state"]


def last_market_change_since(since_date: datetime) -> dict | None:
    """
    Gets the last time the market_State table changed to a particular state.

    Args:
        since_date: Will check for market changes before this date

    Returns: datetime - The datetime of the last market_State change since the specified date. None if no datetime exists
    """

    last_change = (
        supabase.table("market_State")
        .select("changed_last, state")
        .lt("changed_last", to_supabase_date(since_date))
        .order("changed_last", desc=True)
        .limit(1)
        .single()
        .execute()
        .data
    )

    return last_change


def update_user_balance(user_id: str, amount: int) -> int:
    """
    Updates the user's balance by adding the given amount

    Args:
        user_id (str): The user's ID
        amount (int): The amount to add to the user's balance

    Returns: int - The new balance
    """
    old_balance = (
        supabase.table("profiles")
        .select("balance")
        .eq("userId", user_id)
        .execute()
        .data.pop()["balance"]
    )
    new_balance = (
        supabase.table("profiles")
        .update({"balance": old_balance + amount})
        .eq("userId", user_id)
        .execute()
    )
    # make sure in the future that the query executed correctly and return if it didn't
    return new_balance


def update_user_portfolio(user_id: str, stock_id: int, quantity: int) -> int:
    """
    Updates the user's portfolio by adding the given quantity of the stock

    Args:
        user_id (str): The user's ID
        stock_id (int): The stock's ID
        quantity (int): The quantity of the stock to add

    Returns: int - The new quantity of the stock in the user's portfolio
    """
    result = (
        supabase.table("portfolio")
        .select("quantity")
        .eq("userId", user_id)
        .eq("stockId", stock_id)
        .execute()
        .data
    )
    if result:
        old_quantity = result.pop()["quantity"]
        new_quantity = (
            supabase.table("portfolio")
            .update({"quantity": old_quantity + quantity})
            .eq("userId", user_id)
            .eq("stockId", stock_id)
            .execute()
        )
        payload = new_quantity
    else:
        supabase.table("portfolio").insert(
            {"userId": user_id, "stockId": stock_id, "quantity": quantity}
        ).execute()
        payload = quantity
    return payload


def fetch_stock_price(stock_id: int) -> int | None:
    """
    Gets the current stock price of the given stock_id

    Args:
        stock_id (int): The id of the stock you want to get the price of

    Returns: The price of the stock
    """

    result = (
        supabase.table("stock_price")
        .select("stock_price")
        .eq("stockId", stock_id)
        .execute()
        .data
    )

    if result:
        stock_price = result.pop()["stock_price"]
        return stock_price
    return None


def delete_processed_order(order_index: int) -> None:
    """
    Deletes the sell/buy order fufilled in a transaction from the active_buy_sell table

    Args:
        order_index(int): The unique row identifier for an entry in the active_buy_sell table

    Returns: None
    """
    print(order_index)
    supabase.table("active_buy_sell").delete().eq("Id", order_index).execute()


def log_transaction(buy_info: dict, sell_info: dict) -> None:
    """
    Logs tansaction info in the inactive_buy_sell table (Should be called @ the end of order flow)
    Removes the Id column from the buyer & seller info before logging the transaction

    Args:
        buy_info (dict): Data related to the buy side of the transaction
        sell_info (dict): Data relatedto the sell side of the transaction

    Returns: None
    """

    del buy_info["Id"]
    del buy_info["has_been_processed"]
    del sell_info["Id"]
    del sell_info["has_been_processed"]

    supabase.table("inactive_buy_sell").insert(buy_info).execute()
    supabase.table("inactive_buy_sell").insert(sell_info).execute()


def get_expired() -> list[dict]:
    """
    Return a list of active orders that have expired.
    Only contains the order id.
    """

    orders = (
        supabase.table("active_buy_sell")
        .select("Id")
        .lte("expirey", datetime.now().isoformat())
        .order("expirey", desc=False)
        .execute()
    )

    return orders.data


def expire_order(order_id: int):
    """
    Move order_id from active to inactive order table
    Refunds stocks or money
    Args:
        order_id (int): The active order id
    """

    # Delete order
    order = (
        supabase.table("active_buy_sell").delete().eq("Id", order_id).execute()
    ).data[0]

    # Refund stocks/money
    if order["buy_or_sell"]:
        # Buy order - refund money
        order_cost = order["quantity"] * order["price"]

        current_balance = (
            supabase.table("profiles")
            .select("balance")
            .eq("userId", order["userId"])
            .single()
            .execute()
        ).data["balance"]

        supabase.table("profiles").update({"balance": current_balance + order_cost}).eq(
            "userId", order["userId"]
        ).execute()

    else:
        # Sell order - refund stock
        current_amount = (
            supabase.table("portfolio")
            .select("quantity")
            .eq("stockId", order["stockId"])
            .eq("userId", order["userId"])
            .single()
            .execute()
        ).data["quantity"]

        supabase.table("portfolio").update(
            {
                "quantity": current_amount + order["quantity"],
                "price_avg": order["price"],
            }
        ).eq("stockId", order["stockId"]).eq("userId", order["userId"]).execute()

    # Insert record into inactive_buy_sell
    del order["has_been_processed"]
    order["delisted_time"] = datetime.now().isoformat()

    supabase.table("inactive_buy_sell").insert(order).execute()


def get_user_profile(user_id: str) -> dict:
    """
    Get the user's profile from the profiles table

    Args:
        user_id (str): The user's ID

    Returns: dict - The user's profile
    """
    return (
        supabase.table("profiles")
        .select("*")
        .eq("userId", user_id)
        .execute()
        .data.pop()
    )


def get_user_portfolio(user_id: str) -> list[dict]:
    """
    Get the user's portfolio from the portfolio table

    Args:
        user_id (str): The user's ID

    Returns: list[dict] - The user's portfolio
    """
    return supabase.table("portfolio").select("*").eq("userId", user_id).execute().data


def get_user_active_orders(user_id: str) -> list[dict]:
    """
    Get the user's active orders from the active_buy_sell table

    Args:
        user_id (str): The user's ID

    Returns: list[dict] - The user's active orders"""
    return (
        supabase.table("active_buy_sell")
        .select("*")
        .eq("userId", user_id)
        .execute()
        .data
    )


def validate_user(user_id: str):
    """
    Validate that a user exists in the database

    Args:
        user_id (str): The user's ID

    Returns: the user_id if the user exists, an error message otherwise
    """
    return bool(
        supabase.table("profiles").select("*").eq("userId", user_id).execute().data
    )


def migrate_price_changes(hour: datetime):
    """
    Migrates order history

    Args: hour (datetime): The end of the range of time to look at orders.
    For migration into the weekly table, daily table entries with timestamp in the range [hour -1, hour] are looked at.
    """

    current_hour_time = hour.replace(minute=0, second=0, microsecond=0)
    last_hour_time = current_hour_time - timedelta(hours=1)
    two_hours_ago = current_hour_time - timedelta(hours=2)
    last_day_time = current_hour_time - timedelta(days=1)

    all_stock_ids = supabase.table("stock_info").select("id").execute().data
    all_hour_price_changes = (
        supabase.table("stock_price_history_daily")
        .select("changed_at, price, stockId")
        .order("changed_at")
        .order("stockId")
        .gte("changed_at", to_supabase_date(last_hour_time))
        .lt("changed_at", to_supabase_date(current_hour_time))
        .execute()
        .data
    )
    all_hour_fulfilled = (
        supabase.table("inactive_buy_sell")
        .select("quantity, stockId")
        .gte("delisted_time", to_supabase_date(last_hour_time))
        .lt("delisted_time", to_supabase_date(current_hour_time))
        .eq("completed", "TRUE")
        .eq("buy_or_sell", "TRUE")
        .order("stockId")
        .execute()
        .data
    )

    last_weekly_history = (
        supabase.table("stock_price_history_weekly")
        .select("closing_price", "stockId")
        .eq("starting_hour", to_supabase_date(two_hours_ago))
        .execute()
        .data
    )

    hour_volume_table = {}
    hour_change_table = {}
    hour_check_table = {}

    for stock_id in all_stock_ids:
        hour_volume_table[stock_id["id"]] = (0, 0)
        hour_check_table[stock_id["id"]] = False
        hour_change_table[stock_id["id"]] = {
            "starting_hour": to_supabase_date(last_hour_time),
            "stockId": stock_id["id"],
            "average_price": 0,
            "highest_price": 0,
            "lowest_price": 0,
            "opening_price": 0,
            "closing_price": 0,
            "volume_of_sales": 0,
        }

    # Use last the last hours close as the default for this hours open, close, highest, lowest, and average price.
    for weekly_entry in last_weekly_history:
        hour_check_table[weekly_entry["stockId"]] = True
        hour_change_table[weekly_entry["stockId"]]["opening_price"] = weekly_entry[
            "closing_price"
        ]
        hour_change_table[weekly_entry["stockId"]]["closing_price"] = weekly_entry[
            "closing_price"
        ]
        hour_change_table[weekly_entry["stockId"]]["highest_price"] = weekly_entry[
            "closing_price"
        ]
        hour_change_table[weekly_entry["stockId"]]["lowest_price"] = weekly_entry[
            "closing_price"
        ]
        hour_change_table[weekly_entry["stockId"]]["average_price"] = weekly_entry[
            "closing_price"
        ]

    # If there was no weekly entry for the stock, then the stock must be new. In this case, check for the earliest daily entry. Stocks are created with an entry via a database trigger.
    for hour_check in hour_check_table.items():
        if not hour_check[1]:
            stock_weekly_default = (
                supabase.table("stock_price_history_daily")
                .select("price")
                .eq("stockId", hour_check[0])
                .order("changed_at", desc=False)
                .limit(1)
                .single()
                .execute()
                .data
            )

            hour_change_table[hour_check[0]]["opening_price"] = stock_weekly_default[
                "price"
            ]
            hour_change_table[hour_check[0]]["closing_price"] = stock_weekly_default[
                "price"
            ]
            hour_change_table[hour_check[0]]["highest_price"] = stock_weekly_default[
                "price"
            ]
            hour_change_table[hour_check[0]]["lowest_price"] = stock_weekly_default[
                "price"
            ]
            hour_change_table[hour_check[0]]["average_price"] = stock_weekly_default[
                "price"
            ]

    for fulfilled_order in all_hour_fulfilled:
        hour_volume_table[fulfilled_order["stockId"]] += (
            fulfilled_order["quantity"],
            fulfilled_order["quantity"] * fulfilled_order["price"],
        )

    current_stock = all_hour_price_changes[0]["stockId"]
    hour_highest = all_hour_price_changes[0]["price"]
    hour_lowest = all_hour_price_changes[0]["price"]
    hour_last_price = all_hour_price_changes[0]["price"]

    for price_change in all_hour_price_changes:
        if price_change["stockId"] != current_stock:
            hour_change_table[current_stock]["average_price"] = (
                hour_last_price
                if hour_volume_table[current_stock][0] == 0
                else hour_volume_table[current_stock][1]
                / hour_volume_table[current_stock][0]
            )
            hour_change_table[current_stock]["highest_price"] = hour_highest
            hour_change_table[current_stock]["lowest_price"] = hour_lowest
            hour_change_table[current_stock]["closing_price"] = hour_last_price
            hour_change_table[current_stock]["volume_of_sales"] = hour_volume_table[
                current_stock
            ][0]

            current_stock = price_change["stockId"]
            hour_highest = price_change["price"]
            hour_lowest = price_change["price"]
            hour_last_price = price_change["price"]
        else:
            hour_highest = max(hour_highest, price_change["price"])
            hour_lowest = min(hour_lowest, price_change["price"])
            hour_last_price = price_change["price"]

    hour_change_table[current_stock]["average_price"] = (
        hour_last_price
        if hour_volume_table[current_stock][0] == 0
        else hour_volume_table[current_stock][1] / hour_volume_table[current_stock][0]
    )
    hour_change_table[current_stock]["highest_price"] = hour_highest
    hour_change_table[current_stock]["lowest_price"] = hour_lowest
    hour_change_table[current_stock]["closing_price"] = hour_last_price
    hour_change_table[current_stock]["volume_of_sales"] = hour_volume_table[
        current_stock
    ][0]

    supabase.table("stock_price_history_weekly").insert(
        list(hour_change_table.values())
    ).execute()

    # If hour == 0 we're at the end of the day
    if current_hour_time.hour == 0:

        monthly_entries = []
        todays_weekly_entries = (
            supabase.table("stock_price_history_weekly")
            .select(
                "opening_price",
                "closing_price",
                "stockId",
                "average_price",
                "volume_of_sales",
                "lowest_price",
                "highest_price",
            )
            .gte("starting_hour", to_supabase_date(last_day_time))
            .lt("starting_hour", to_supabase_date(current_hour_time))
            .order("starting_hour")
            .order("stockId")
            .execute()
            .data
        )

        # We do a little grouping
        weekly_group_table = {}

        for weekly_entry in todays_weekly_entries:
            if weekly_entry["stockId"] not in weekly_group_table:
                weekly_group_table[weekly_entry["stockId"]] = [weekly_entry]
            else:
                weekly_group_table[weekly_entry["stockId"]] += [weekly_entry]

        print(weekly_group_table)
        print(weekly_group_table.keys())
        pprint.pprint(weekly_group_table)
        for stock_group in list(weekly_group_table.values()):
            current_stock_id = stock_group[0]["stockId"]
            open_price = stock_group[0]["opening_price"]
            highest_price = stock_group[0]["highest_price"]
            lowest_price = stock_group[0]["lowest_price"]
            closing_price = stock_group[len(stock_group) - 1]["closing_price"]
            total_volume = 0
            total_price_sum = 0

            for weekly_entry in stock_group:
                total_volume += weekly_entry["volume_of_sales"]
                total_price_sum += (
                    weekly_entry["average_price"] * weekly_entry["volume_of_sales"]
                )

                highest_price = max(highest_price, weekly_entry["highest_price"])
                lowest_price = min(lowest_price, weekly_entry["lowest_price"])

            monthly_entries += [
                {
                    "starting_hour": to_supabase_date(
                        current_hour_time - timedelta(days=1)
                    ),
                    "stockId": current_stock_id,
                    "opening_price": open_price,
                    "closing_price": closing_price,
                    "highest_price": highest_price,
                    "lowest_price": lowest_price,
                    "volume_of_sales": total_volume,
                    "average_price": (
                        (total_price_sum / total_volume)
                        if total_volume != 0
                        else open_price
                    ),
                }
            ]
        supabase.table("stock_price_history_monthly").insert(monthly_entries).execute()

        # Delete old weekly entries
        old_weekly_hours = (
            supabase.table("stock_price_history_weekly")
            .select("starting_hour")
            .lt("starting_hour", to_supabase_date(current_hour_time))
            .order("starting_hour", desc=True)
            .execute()
            .data
        )

        old_days = set()
        for old_weekly_hour in old_weekly_hours:
            test_day = from_supabase_date(old_weekly_hour["starting_hour"]).replace(
                hour=0,
                minute=0,
            )
            if test_day not in old_days:
                old_days.add(test_day)
        print(old_days)
        if len(old_days) > 7:
            oldest_day = last_day_time
            for old_day in old_days:
                oldest_day = min(oldest_day, old_day)

            (
                supabase.table("stock_price_history_weekly")
                .delete()
                .lt("starting_hour", to_supabase_date(oldest_day + timedelta(days=1)))
                .execute()
            )
