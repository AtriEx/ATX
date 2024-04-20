"""
Handles migrating order history every hour. Moves order history from daily to weekly every hour. 
Moves order history from weekly to monthly every day.
Checks to see if an hour has passed every minute (avoids an hour timer missing an hour)
"""

import os
import threading
from datetime import datetime

from dotenv import find_dotenv, load_dotenv

from database import supabase_middleman
from util.date_extensions import from_supabase_date

load_dotenv(os.getenv("ENV_FILE", find_dotenv()))

# Should be set to one minute in production although any number under one hour will ensure
# migration never skips an hour.
MIGRATION_SLEEP_TIME = int(
    os.getenv("MIGRATION_LOOP_DELAY", "0")
)  # If 0, don't do the loop


class MigrateOrderHistoryThread(threading.Thread):
    """Infinitely running thread to migrate order history."""

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        """Stop the thread after completing db operations."""
        super().__init__()
        self._stop_event.set()

    def run(self):
        """Runs a loop that checks if we should migrate orders,
        then migrates orders if those checks pass"""

        if MIGRATION_SLEEP_TIME == 0:
            return

        last_hour = datetime.now().replace(minute=0, second=0, microsecond=0)

        while not self._stop_event.is_set():
            current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
            if last_hour != current_hour:
                market_change = supabase_middleman.last_market_change_since(
                    current_hour
                )
                # If the last market change was an open then the market must have opened in the
                # last hour and we should migrate order history changes.Otherwise, if the last
                # market change was a close and occurred between the last hour and now, then the
                # market was open during the last hour and we should migrate order history changes.
                if market_change is not None and (
                    market_change["state"]
                    or (
                        from_supabase_date(market_change["changed_last"]) > last_hour
                        and not market_change["state"]
                    )
                ):
                    supabase_middleman.migrate_price_changes(current_hour)
                last_hour = current_hour
            self._stop_event.wait(MIGRATION_SLEEP_TIME)
