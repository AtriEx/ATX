from typing import Literal
from supabase import create_client, Client

url = "https://wxskoymvdulyscwhebze.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind4c2tveW12ZHVseXNjd2hlYnplIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNjY2NTAzMywiZXhwIjoyMDIyMjQxMDMzfQ.HaBk3QEcnHJaJ284RmHK49fMXmEPzTJHDvzwoQ-eRt0"
supabase: Client = create_client(url, key)


def fetch_entries():
    pass


def fetch_user_data(
    userID: str, portfolioOrProfiles: Literal["portfolio", "profiles"]
) -> dict:
    """
    Fetches user data from either Portfolio or profiles table using userId

    Args:
        userID (str): The ID of the user
        portfolioOrProfiles (str): Specifies the table to fetch from. Must be 'portfolio' or 'profiles'.

    Raises:
        ValueError: If portfolioOrProfiles is not 'Porfolio' or 'profiles'.

    Returns: dictionary of the values
    """

    if portfolioOrProfiles not in ["Portfolio", "profiles"]:
        raise ValueError(
            "portfolioOrProfiles must be either 'Portfolio' or 'profiles'."
        )

    return (
        supabase.table(f"{portfolioOrProfiles}")
        .select("*")
        .eq("userId", userID)
        .execute()
        .data
    )


def insert_stock_in_portfolio(portfolioSupabase, quantity, userID):
    pass


def update_entry():
    pass
