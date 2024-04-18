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

    thread.start()
    yield  # Anything after here runs when server is shutting down
    thread.stop()


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

