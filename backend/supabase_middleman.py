from typing import Literal
from supabase import create_client, Client

url = "https://wxskoymvdulyscwhebze.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind4c2tveW12ZHVseXNjd2hlYnplIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNjY2NTAzMywiZXhwIjoyMDIyMjQxMDMzfQ.HaBk3QEcnHJaJ284RmHK49fMXmEPzTJHDvzwoQ-eRt0"
supabase: Client = create_client(url, key)


def fetch_entries():
    pass


def fetch_user_data(
    user_id: str, portfolio_or_profiles: Literal["portfolio", "profiles"]
) -> dict:
    """
    Fetches user data from either Portfolio or profiles table using userId

    Args:
        user_id (str): The ID of the user
        portfolio_or_profiles (str): Specifies the table to fetch from. Must be 'portfolio' or 'profiles'.

    Raises:
        ValueError: If portfolio_or_profiles is not 'porfolio' or 'profiles'.

    Returns: dictionary of the values
    """

    if portfolio_or_profiles not in ["portfolio", "profiles"]:
        raise ValueError(
            "portfolio_or_profiles must be either 'portfolio' or 'profiles'."
        )

    return (
        supabase.table(f"{portfolio_or_profiles}")
        .select("*")
        .eq("userId", user_id)
        .execute()
        .data
    )


def insert_stock_in_portfolio(portfolio_supabase, quantity, user_id):
    pass


def update_entry():
    pass
