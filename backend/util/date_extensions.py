from datetime import datetime


def from_supabase_date(date: str) -> datetime:
    return datetime.strptime(date, "%y-%m-%dT%H:%M:%S")

def to_supabase_date(date: datetime) -> str:
    return datetime.strftime("%y-%m-%d %H:%M:%S")

