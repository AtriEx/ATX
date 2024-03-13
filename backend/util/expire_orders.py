"""
Handles orders moving from the active to inactive buy orders table once it
has expired.
"""

import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from database import supabase_middleman

load_dotenv(find_dotenv())

SLEEP_TIME = int(os.getenv("EXPIRE_LOOP_DELAY", 10))  # Default to 10s


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Runs before and after the server starts and closes"""
    task = asyncio.create_task(run_loop())
    yield  # Anything after here runs when server is shutting down
    task.cancel()


async def run_loop():
    """Infinetly runs a loop to expire orders."""

    await asyncio.sleep(5)  # Allow server to start

    while True:
        orders = supabase_middleman.get_active()

        for order in orders:
            # expirey column is optional
            try:
                expiry_time = datetime.fromisoformat(order["expirey"])
            except KeyError:
                continue

            # Since it's sorted, all orders after are also in the future
            if expiry_time > datetime.now():
                break

            await supabase_middleman.expire_order(order["Id"])

        await asyncio.sleep(SLEEP_TIME)
