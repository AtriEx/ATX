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



@app.get('/buyOrder')
def test_entry_1():
    create_active_order.create_buy_order()
    return "Test entry inserted"


@app.get('/qb')
def create_buy_order():
    buy_order.buy_order()
    return "Quick buy executed"
