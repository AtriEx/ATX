"""API routes declaration"""

from fastapi import FastAPI

from database import supabase_middleman
from routes import buy_order, create_active_order, net_worth_calculator
from util.expire_orders import lifespan

app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    """API route for health checks."""
    return ""


# testing
@app.get("/buyOrder")
def test_entry_1():
    """API route for creating a test buy order."""
    # create_active_order.create_sell_order()
    return "Test entry inserted"


# prod
@app.get("/qb")
def create_buy_order(data: dict):
    """API route for creating a buy order for one share of a stock."""
    ret_val = buy_order.buy_order(data)
    return ret_val


# testing
@app.get("/testParams")
def test_params(data: dict):
    """API route for testing parameters."""
    buy_order.test_params()
    return data


# testing
@app.get("/insertCustomOrder")
def insert_custom_order(data: dict):
    """API route for inserting a custom order."""
    supabase_middleman.insert_entry("active_buy_sell", data)
    return "Custom order inserted"


# testing
@app.get("/changeBalanceTest")
def change_balance_test(amount: int):
    """API route for testing balance changes."""
    output = supabase_middleman.update_user_balance(
        "36d22a68-ca25-4110-b769-44cf5b4a1c89", amount
    )
    return output


# prod
@app.get("/netWorth")
def fetch_net_worth(user_id: str):
    """API route for calculating the net worth of a user."""
    net_worth = net_worth_calculator.net_worth_calculator(user_id)
    return net_worth


# prod
@app.get("/createActiveOrder")
def create_order(data: dict):
    """API route for creating an active order."""
    create_active_order.create_active_buy_sell_order(data)
    return "Active order created"
