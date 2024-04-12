"""
Handles orders moving from the active to inactive buy orders table once it
has expired.
"""

from datetime import datetime
import os
import threading
from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from database import supabase_middleman

load_dotenv(os.getenv("ENV_FILE", find_dotenv()))

SLEEP_TIME = int(os.getenv("EXPIRE_LOOP_DELAY", "0"))  # If 0, don't do the loop

MIGRATION_SLEEP_TIME = int(os.getenv("MIGRATION_LOOP_DELAY", "0"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Runs before and after the server starts and closes"""
    thread = ExpireOrdersThread()
    migration_thread = MigrateOrderHistoryThread()

    thread.start()
    migration_thread.start()
    yield  # Anything after here runs when server is shutting down
    thread.stop()
    migration_thread.stop()


class ExpireOrdersThread(threading.Thread):
    """Infinetly running thread to expire orders."""

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        """Stop the thread after completing db operations."""
        self._stop_event.set()

    def run(self):
        """Infinetly runs a loop to expire orders."""

        if SLEEP_TIME == 0:
            return

        # Will complete db operations before shutting down
        while not self._stop_event.is_set():
            orders = supabase_middleman.get_expired()

            for order in orders:
                supabase_middleman.expire_order(order["Id"])

            self._stop_event.wait(SLEEP_TIME)

class MigrateOrderHistoryThread(threading.Thread):
    """Infinitely running thread to migrate orders."""
    
    def __init__ (self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        super().__init__()
        self._stop_event.set()

    def run(self):
        """"""

        if MIGRATION_SLEEP_TIME  == 0:
            return

        last_migrated_hour = None

        

        while not self._stop_event.is_set():
            current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
            if last_migrated_hour != current_hour:
                supabase_middleman.migrate_price_changes(current_hour)
                last_migrated_hour = current_hour
            self._stop_event.wait(MIGRATION_SLEEP_TIME)
