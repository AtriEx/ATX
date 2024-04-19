"""Utility date functions for dealing with supabase date strings"""

from datetime import datetime


def from_supabase_date(date: str) -> datetime:
    """
    Converts a supabase date/timestamp into a python datetime

    Args:
        date (str): The date/timestamp retrieved from supabase
    Returns: datetime
    """
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


def to_supabase_date(date: datetime) -> str:
    """
    Converts a python datetime into a supabase date/timestamp string

    Args:
        date (datetime): The date/timestamp retrieved from supabase
    Returns: supabase timestamp string
    """
    return datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
