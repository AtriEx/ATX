# from routers import items, users
from datetime import datetime, timedelta
from fastapi import FastAPI
from supabase import create_client, Client
from database.supabase.store import supabase_middleman
from routes.api import create_active_order
from routes.api import buy_order
from dotenv import load_dotenv
import os


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
def create_active_order(
    buy_or_sell: bool,
    price: int,
    expirey: datetime,
    quantity: int,
    stockId: int,
    userId: str,
):
    if price < 1:
        return "Price must be greater than 0"
    if quantity < 1:
        return "Quantity must be greater than 0"
    if expirey < datetime.now():
        return "Expirey must be in the future"
    if stockId < 1:  # TODO determine what is valid stockId
        return "Invalid stockId"
    if userId == "":  # TODO determine what is valid userId
        return "Invalid userId"
    time_posted = datetime.now().isoformat()
    create_active_order.create_active_order(
        time_posted, buy_or_sell, price, expirey, quantity, stockId, userId
    )
    return "Active order created"
