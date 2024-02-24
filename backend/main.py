from datetime import datetime, timedelta
from fastapi import FastAPI
# pylint: disable=no-name-in-module # it's looking in the supabase folder in project root
from supabase import create_client, Client
from database import supabase_middleman
from routes import create_active_order
from routes import buy_order
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
