"""This module implements commonly-used supabase operations as functions."""

from typing import Literal

# pylint: disable=no-name-in-module
from supabase import create_client, Client

URL = "https://wxskoymvdulyscwhebze.supabase.co"
# TODO: put in config?
# pylint: disable=line-too-long
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind4c2tveW12ZHVseXNjd2hlYnplIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNjY2NTAzMywiZXhwIjoyMDIyMjQxMDMzfQ.HaBk3QEcnHJaJ284RmHK49fMXmEPzTJHDvzwoQ-eRt0"
SUPABASE: Client = create_client(URL, KEY)


# def fetch_entries():
#     pass


def fetchUserData(
    userId: str, portfolioOrProfiles: Literal["portfolio", "profiles"]
) -> dict:
    """
    Fetches user data from either Portfolio or profiles table using userId

    Args:
        user_id (str): The ID of the user
        portfolioOrProfiles (str): Specifies the table to fetch from.
            Must be 'portfolio' or 'profiles'.

    Raises:
        ValueError: If portfolioOrProfiles is not 'porfolio' or 'profiles'.

    Returns: dictionary of the values
    """

    if portfolioOrProfiles not in ["portfolio", "profiles"]:
        raise ValueError(
            "portfolioOrProfiles must be either 'portfolio' or 'profiles'."
        )

    return (
        SUPABASE.table(f"{portfolioOrProfiles}")
        .select("*")
        .eq("userId", userId)
        .execute()
        .data
    )


# def insert_stock_in_portfolio(portfolio_supabase, quantity, user_id):
#     pass


# def update_entry():
#     pass
