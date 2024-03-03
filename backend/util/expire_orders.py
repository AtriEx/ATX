"""
Handles orders moving from the active to inactive buy orders table once it
has expired.
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI

from database import supabase_middleman


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(run_loop())
    yield
    task.cancel()


async def run_loop():
    """Infinetly runs a loop to expire orders."""
    while True:
        orders = supabase_middleman.get_active()

        for order in orders:
            expiry_time = datetime.fromisoformat(order["expirey"])

            # Since it's sorted, all orders after are also in the future
            if expiry_time > datetime.now():
                break

            # TODO
            # Make it inactive

        await asyncio.sleep(10)
