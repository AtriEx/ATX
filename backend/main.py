# from routers import items, users
from datetime import datetime, timedelta
from fastapi import FastAPI
from supabase import create_client, Client
from database.supabase.store import supabase_middleman
from routes.api import create_active_order
from routes.api import buy_order
from dotenv import load_dotenv
import os
from uuid import UUID

app = FastAPI()


@app.get("/buyOrder")
def test_entry_1():
    create_active_order.create_buy_order()
    return "Test entry inserted"


@app.get("/qb")
def create_buy_order():
    buy_order.buy_order()
    return "Quick buy executed"


@app.get("/createActiveOrder")
def create_active_buy_sell_order(
    buy_or_sell: bool,
    price: int,
    expirey: datetime,
    quantity: int,
    stock_id: int,
    user_id: str,
):
    if price < 1:
        return "Price must be greater than 0"
    if quantity < 1:
        return "Quantity must be greater than 0"
    if expirey < datetime.now():
        return "Expirey must be in the future"

    if not supabase_middleman.fetch_stock_price(stock_id):
        return "Stock not found"

    # validate user_id is a valid uuid and it exists
    try:
        UUID(hex=user_id)  # throws value error if not a valid uuid
        user_profile = supabase_middleman.fetch_profile(user_id)
        if not user_profile:
            return "User not found"
    except ValueError:
        return "userId not in UUID format"

    # validate that if order is a buy order, user has enough balance, or if order is a sell order, user has enough quantity
    if buy_or_sell:  # Buy order
        user_profile = supabase_middleman.fetch_profile(user_id)
        if not user_profile:
            return "User not found"
        if user_profile["balance"] < price * quantity:
            return "Insufficient funds"
    else:  # Sell order
        portfolio = supabase_middleman.fetch_portfolio(user_id, stock_id)
        if not portfolio:
            return "Portfolio not found"
        if portfolio["quantity"] < 1:
            return "User does not own this stock"
        if portfolio["quantity"] < quantity:
            return "Insufficient quantity"

    time_posted = datetime.now().isoformat()
    create_active_order.create_active_order(
        time_posted, buy_or_sell, price, expirey, quantity, stock_id, user_id
    )
    return "Active order created"
