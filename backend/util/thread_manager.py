"""
Creates threads that start running before the server starts and shutdown after the server closes.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from expire_orders import ExpireOrdersThread
from migrate_history import MigrateOrderHistoryThread

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Runs before and after the server starts and closes"""
    history_migration_thread = MigrateOrderHistoryThread()
    order_expiration_thread = ExpireOrdersThread()

    history_migration_thread.start()
    order_expiration_thread.start()
    yield  # Anything after here runs when server is shutting down
    history_migration_thread.stop()
    order_expiration_thread.stop()
