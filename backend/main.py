"""API routes declaration"""

from fastapi import FastAPI

from routes import buy_order, create_active_order

from database import supabase_middleman

app = FastAPI()


@app.get("/buyOrder")
def test_entry_1():
    """API route for creating a test buy order."""
    create_active_order.create_buy_order()
    return "Test entry inserted"


@app.get("/qb")
def create_buy_order(data : dict):
    """API route for creating a buy order for one share of a stock."""
    ret_val=buy_order.buy_order(data)
    return ret_val

@app.get("/testParams")
def test_params(data: dict):
    """API route for testing parameters."""
    buy_order.test_params()
    return data

@app.get("/insertCustomOrder")
def insert_custom_order(data: dict):
    """API route for inserting a custom order."""
    supabase_middleman.insert_entry("active_buy_sell", data)
    return "Custom order inserted"