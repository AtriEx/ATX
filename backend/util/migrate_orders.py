import os
import threading
from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from database import supabase_middleman

load_dotenv(os.getenv("ENV_FILE", find_dotenv()))

SLEEP_TIME = int(os.getenv("MIGRATE_LOOP_DELAY", "0"))  # If 0, don't do the loop


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Runs before and after the server starts and closes"""
    thread = ExpireOrdersThread()

    thread.start()
    yield  # Anything after here runs when server is shutting down
    thread.stop()
