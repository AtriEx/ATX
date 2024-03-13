"""
Handles orders moving from the active to inactive buy orders table once it
has expired.
"""

import os
import threading
import time
from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from database import supabase_middleman

load_dotenv(find_dotenv())

SLEEP_TIME = int(os.getenv("EXPIRE_LOOP_DELAY", "10"))  # Default to 10s


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

        # Will complete db operations before shutting down
        while not self._stop_event.is_set():
            orders = supabase_middleman.get_expired()

            for order in orders:
                supabase_middleman.expire_order(order["Id"])

            # Server may have stopped during db operations
            if not self._stop_event.is_set():
                time.sleep(SLEEP_TIME)
