"""API routes declaration"""

from fastapi import FastAPI

from routes import buy_order, create_active_order
from util.expire_orders import lifespan

app = FastAPI(lifespan=lifespan)


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
