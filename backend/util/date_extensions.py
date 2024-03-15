from datetime import datetime


def from_supabase_date(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

def to_supabase_date(date: datetime) -> str:
    return datetime.strftime(date, "%Y-%m-%d %H:%M:%S")

