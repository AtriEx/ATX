import os
from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from util.ext import test_data
from database import supabase_middleman

app=FastAPI()
load_dotenv()


#
def create_buy_order():
    # Insert a test entry into the active_buy_sell table
    test_entry = test_data.test_entry_1()
    supabase_middleman.insert_entry('active_buy_sell', test_entry)
    return 

def create_sell_order():
    # Insert a test entry into the active_buy_sell table
    test_entry = test_data.test_entry_2()
    supabase_middleman.insert_entry('active_buy_sell', test_entry)
    return
