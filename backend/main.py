"""API routes declaration"""

from fastapi import FastAPI

from routes import buy_order, create_active_order
from util import test_history_migration

app = FastAPI()


@app.get("/buyOrder")
def test_entry_1():
    """API route for creating a test buy order."""
    create_active_order.create_buy_order()
    return "Test entry inserted"


@app.get("/qb")
def create_buy_order():
    """API route for creating a buy order for one share of a stock."""
    buy_order.buy_order()
    return "Quick buy executed"

@app.get("/migrateHistory")
def test_history_route():
    test_history_migration.test_migrate_history_middle_day()
